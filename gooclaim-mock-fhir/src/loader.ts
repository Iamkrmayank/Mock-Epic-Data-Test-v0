/**
 * Fixture loader - reads JSON files and detects Bundle vs single resource
 */

import * as fs from 'fs';
import * as path from 'path';
import { isBundle, FHIRResource, FHIRBundle } from './fhir';

const RESOURCE_MAP: Record<string, string[]> = {
  Patient: ["patient.json"],
  Coverage: ["coverage.json"],
  Encounter: ["encounterr.json", "encounter.json"],
  Appointment: ["appointments.json", "appointment.json"],
  Contract: ["contract.json"],
  Consent: ["consent.json"],
  DocumentReference: ["docref.json", "documentreference.json"],
  Condition: ["conditionss.json", "condition.json"],
  Procedure: ["procedure.json"],
  Observation: ["observation.json"],
  Binary: ["binary.json"],
  Organization: ["organisation.json", "organization.json"],
  Practitioner: ["practitioner.json"],
  PractitionerRole: ["practitionerrole.json", "practitionerRole.json"],
  ExplanationOfBenefit: ["eob.json"],
  Provenance: ["provenance.json"]
} as const;

export class FixtureLoader {
  private fixtureDir: string;
  private cache: Map<string, any> = new Map();

  constructor(fixtureDir: string) {
    this.fixtureDir = fixtureDir;
  }

  /**
   * Get the fixture file path for a resource type
   */
  private getFixturePath(resourceType: string): string | null {
    const candidates = RESOURCE_MAP[resourceType];
    if (!candidates) {
      return null;
    }

    for (const filename of candidates) {
      const filePath = path.join(this.fixtureDir, filename);
      if (fs.existsSync(filePath)) {
        return filePath;
      }
    }

    return null;
  }

  /**
   * Load fixture data from file
   */
  private loadFixture(filePath: string): any {
    // Check cache first
    if (this.cache.has(filePath)) {
      return this.cache.get(filePath);
    }

    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const data = JSON.parse(content);
      this.cache.set(filePath, data);
      return data;
    } catch (error) {
      console.error(`Error loading fixture ${filePath}:`, error);
      return null;
    }
  }

  /**
   * Get resource by type and optional ID
   */
  getResource(resourceType: string, id?: string): FHIRResource | FHIRBundle | null {
    const filePath = this.getFixturePath(resourceType);
    if (!filePath) {
      return null;
    }

    const data = this.loadFixture(filePath);
    if (!data) {
      return null;
    }

    // Handle different JSON structures
    // 1. Direct FHIR resource
    if (data.resourceType === resourceType) {
      if (id && data.id !== id) {
        return null; // ID mismatch
      }
      return data;
    }

    // 2. Bundle with appointments array (special case for appointments.json)
    if (resourceType === "Appointment" && Array.isArray(data.appointments)) {
      if (id) {
        const appointment = data.appointments.find((apt: any) => apt.id === id);
        if (!appointment) return null;
        return {
          resourceType: "Appointment",
          id: appointment.id,
          status: appointment.status,
          description: appointment.description,
          start: appointment.start,
          end: appointment.end,
          duration: appointment.duration,
          serviceType: appointment.service_type,
          participants: appointment.participants,
          location: appointment.location
        };
      }
      // Return bundle
      const entries = data.appointments.slice(0, 25).map((apt: any) => ({
        resource: {
          resourceType: "Appointment",
          id: apt.id,
          status: apt.status,
          description: apt.description
        }
      }));
      return {
        resourceType: "Bundle",
        type: "searchset",
        total: data.total || entries.length,
        entry: entries
      };
    }

    // 3. Data wrapped in "data" key
    if (data.data && data.data.resourceType === resourceType) {
      const resource = data.data;
      if (id && resource.id !== id) {
        return null;
      }
      return resource;
    }

    // 4. Bundle
    if (isBundle(data)) {
      if (id) {
        // Find resource in bundle by ID
        const entry = data.entry?.find(e => e.resource?.id === id);
        return entry?.resource || null;
      }
      return data;
    }

    return null;
  }

  /**
   * Get all resource types
   */
  getResourceTypes(): string[] {
    return Object.keys(RESOURCE_MAP);
  }
}

