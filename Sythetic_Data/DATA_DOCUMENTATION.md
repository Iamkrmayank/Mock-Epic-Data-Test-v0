# Synthetic FHIR R4 Data Documentation

## Overview

This directory contains HIPAA-safe synthetic FHIR R4 test data for an EPIC-like mock server. All data is fictional and generated deterministically to maintain consistency across resources.

**Generated Date**: 2025-01-XX  
**FHIR Version**: R4  
**Total Resources**: ~350+ resources across 15 resource types

---

## Resource Summary

### Core Resources

| Resource Type | File Name | Count | Format | Description |
|--------------|-----------|-------|--------|--------------|
| **Patient** | `patients.json` | 10 | Array | Core patient demographics and identifiers |
| **Organization** | `organisation.json` | 10 | Array | Healthcare organizations and locations |
| **Coverage** | `coverage.json` | 10 | Object with array | Insurance coverage information |
| **Practitioner** | `practitioner.json` | 10 | Array | Healthcare providers |
| **PractitionerRole** | `practitonerrole.json` | 15 | Array | Practitioner roles and specialties |
| **Encounter** | `encounterr.json` | 31 | Bundle | Patient encounters and visits |
| **Procedure** | `procedure.json` | 20 | Bundle | Medical procedures and surgeries |
| **Observation** | `observation.json` | 43 | Array | Lab results and vital signs |
| **Condition** | `conditionss.json` | 32 | Bundle | Medical conditions and diagnoses |
| **DocumentReference** | `docref.json` | 33 | Array | Clinical documents and reports |
| **Consent** | `consent.json` | 31 | Bundle | Patient consents and authorizations |
| **Binary** | `binary.json` | 46 | Array | Binary document content |
| **Appointment** | `appointments.json` | 10 | Bundle | Scheduled appointments |
| **ExplanationOfBenefit** | `eob.json` | 0 | Bundle | EOB (empty with OperationOutcome) |
| **Provenance** | `provenance.json` | 30 | Array | Data provenance and audit trail |

**Total**: 321 individual resources + 10 appointments

---

## Patient IDs (Fixed)

The following Patient IDs are preserved exactly as provided:

1. `ePtdJFCrnl2edlBDdz1C5Ja`
2. `ePt2RJtBRnlWmTSHf6pWkLUy`
3. `ePtfDLkDmWJ6UuVTAIjvFu7`
4. `ePtICPhDeOZIiBOB-Y6sHrFH2ZUC`
5. `ePt-lgotu2iXW7GboIRoL3u6`
6. `ePtHwnMztVuaP.coUNEhEk`
7. `ePt.iqq8vH2BzNZV45pFCiR`
8. `ePtDCajhDieQjEJ.Bq8F80`
9. `ePtmm3T207gmhZRnFyy5r2xJ7`
10. `ePtj4mgblEv0.9BZhvWaXH6K2`

---

## Organization IDs (Fixed)

The following Organization IDs are preserved exactly as provided:

1. `eLJ.EJ4jKEIQOkrtDXtBi10Q71hA1XcW9a`
2. `eLGk8cgSCifdFzctEq8oB7GVvouNndNWYzjFn`
3. `eLMX1C.CI3.dXRZv7qdYdk2r7xgHWPB6PRWJ`
4. `eLpfS2ViRb1.n3U6t3wI973IPFlJ5F7WRd-`
5. `eLDpyOpxyB9JKmyLDUwMbqJfgLq.nbK894R`
6. `eLI-4kf3PGdlDcIfw84Jx3.l8S0QPnuQ0-KZe`
7. `eLx.BTHRJJbykE0.E8.5clLCZFNV8S2QT6IN`
8. `eLgG9oiZ.jgttMkFp1CW54M2NhmABHkuE`
9. `eLjua058LeDKK6jDHz2oCtIsjhvNK4p7M`
10. `eLlOGPoZa70gyU-4gAIqK4.pdEuNb0lCo7pt-L`

---

## Cross-Resource References

### Patient References

All resources that reference patients use the format: `Patient/{PatientID}`

**Resources referencing Patients:**
- ✅ **Coverage**: `beneficiary` field → `Patient/{PatientID}`
- ✅ **Encounter**: `subject` field → `Patient/{PatientID}`
- ✅ **Procedure**: `subject` field → `Patient/{PatientID}`
- ✅ **Observation**: `subject` field → `Patient/{PatientID}`
- ✅ **Condition**: `subject` field → `Patient/{PatientID}`
- ✅ **DocumentReference**: `subject` field → `Patient/{PatientID}`
- ✅ **Consent**: `patient` field → `Patient/{PatientID}`
- ✅ **Appointment**: `participant.actor` → `Patient/{PatientID}`

### Organization References

All resources that reference organizations use the format: `Organization/{OrganizationID}`

**Resources referencing Organizations:**
- ✅ **Patient**: `managingOrganization.reference` → `Organization/{OrgID}`
- ✅ **Coverage**: `payor[0].reference` → `Organization/{OrgID}`
- ✅ **Encounter**: `serviceProvider.reference` → `Organization/{OrgID}`
- ✅ **PractitionerRole**: `location[0].reference` → `Location/{OrgID}` (uses Org ID as Location)

### Practitioner References

**Resources referencing Practitioners:**
- ✅ **PractitionerRole**: `practitioner.reference` → `Practitioner/{PractitionerID}`
- ✅ **Encounter**: `participant[].individual.reference` → `Practitioner/{PractitionerID}`
- ✅ **DocumentReference**: `author[].reference` → `Practitioner/{PractitionerID}`
- ✅ **Provenance**: `agent[].who.reference` → `Practitioner/{PractitionerID}`

### Encounter References

**Resources referencing Encounters:**
- ✅ **Observation**: `encounter.reference` → `Encounter/{EncounterID}`
- ✅ **Procedure**: Linked to encounters through patient context
- ✅ **Condition**: Some conditions linked via `provision.data.reference`

### Coverage References

**Coverage Structure:**
- `id`: Format `cov-{PatientID}`
- `beneficiary`: `Patient/{PatientID}`
- `payor[0].reference`: `Organization/{OrgID}`
- `class[].type.code`: "plan" or "group"
- `class[].value`: Plan code derived from Patient ID

---

## Resource Details

### 1. Patient Resources (`patients.json`)

**Structure**: Array of Patient resources with wrapper

**Key Fields:**
- `resourceType`: "Patient"
- `id`: Patient ID (preserved)
- `data.resourceType`: "Patient"
- `data.extension[]`: Legal sex, race, ethnicity, US Core extensions
- `data.identifier[]`: MRN (urn:mrn:gooclaim), FHIR STU3 ID, Insurance Member ID
- `data.active`: true
- `data.name[]`: Official and usual names
- `data.gender`: "male" or "female"
- `data.birthDate`: Ages 18-85
- `data.address[]`: Realistic US addresses
- `data.telecom[]`: US phone numbers
- `data.managingOrganization.reference`: `Organization/{OrgID}`
- `retrieved_at`: ISO timestamp

**Count**: 10 patients

---

### 2. Organization Resources (`organisation.json`)

**Structure**: Array of Organization resources

**Key Fields:**
- `resourceType`: "Organization"
- `id`: Organization ID (preserved)
- `identifier[]`: NPI, TAX ID, internal IDs
- `active`: true
- `name`: Hospital/clinic names
- `address[]`: Realistic US addresses

**Count**: 10 organizations

---

### 3. Coverage Resources (`coverage.json`)

**Structure**: Object with `total` and `coverage` array

**Key Fields:**
- `total`: Number of coverage entries
- `coverage[].id`: `cov-{PatientID}`
- `coverage[].status`: "active"
- `coverage[].beneficiary`: `Patient/{PatientID}`
- `coverage[].payor[].reference`: `Organization/{OrgID}`
- `coverage[].class[]`: Plan and group codes

**Count**: 10 coverages (one per patient)

---

### 4. Practitioner Resources (`practitioner.json`)

**Structure**: Array of Practitioner resources

**Key Fields:**
- `resourceType`: "Practitioner"
- `id`: Generated ID (ePract...)
- `identifier[]`: NPI, PROVID codes
- `active`: true
- `name[]`: Professional names with MD suffix
- `qualification[]`: MD qualification

**Count**: 10 practitioners

**Specialties**: Cardiology, Internal Medicine, Family Practice, Pediatrics, Orthopedics, General Surgery

---

### 5. PractitionerRole Resources (`practitonerrole.json`)

**Structure**: Array of PractitionerRole resources

**Key Fields:**
- `resourceType`: "PractitionerRole"
- `id`: Generated ID (ePractRole...)
- `active`: true
- `practitioner.reference`: `Practitioner/{PractitionerID}`
- `code[]`: Role codes with SNOMED
- `specialty[]`: Specialty coding
- `location[].reference`: `Location/{OrgID}` (uses Org ID)
- `telecom[]`: Phone numbers

**Count**: 15 practitioner roles (1-2 roles per practitioner)

---

### 6. Encounter Resources (`encounterr.json`)

**Structure**: FHIR Bundle with entries

**Key Fields:**
- `resourceType`: "Bundle"
- `type`: "searchset"
- `total`: Number of encounters
- `entry[].resource.resourceType`: "Encounter"
- `entry[].resource.id`: Generated ID (eEnc...)
- `entry[].resource.status`: planned, arrived, in-progress, finished, etc.
- `entry[].resource.class`: Encounter class (AMB, EMER, IMP, etc.)
- `entry[].resource.type[]`: Encounter types
- `entry[].resource.subject.reference`: `Patient/{PatientID}`
- `entry[].resource.participant[]`: Practitioner references
- `entry[].resource.period`: Start and end times
- `entry[].resource.serviceProvider.reference`: `Organization/{OrgID}`
- `entry[].resource.location[]`: Location references

**Count**: 31 encounters (2-4 per patient)

**Date Range**: 1-18 months ago

---

### 7. Procedure Resources (`procedure.json`)

**Structure**: FHIR Bundle with entries

**Key Fields:**
- `resourceType`: "Bundle"
- `type`: "searchset"
- `entry[].resource.resourceType`: "Procedure"
- `entry[].resource.id`: Generated ID (eProc...)
- `entry[].resource.status`: completed, not-done, in-progress, etc.
- `entry[].resource.category`: Surgical, Diagnostic, Evaluation
- `entry[].resource.code.text`: Procedure name
- `entry[].resource.subject.reference`: `Patient/{PatientID}`
- `entry[].resource.performedDateTime`: Date performed

**Count**: 20 procedures (1-3 per patient)

**Types**: Cesarean Section, Appendectomy, Knee Replacement, Colonoscopy, etc.

---

### 8. Observation Resources (`observation.json`)

**Structure**: Array of Observation resources

**Key Fields:**
- `resourceType`: "Observation"
- `id`: Generated ID (eObs...)
- `status`: final, preliminary, etc.
- `category[]`: Laboratory, Vital Signs, Imaging, Survey
- `code`: LOINC codes (Blood Pressure, Heart Rate, Glucose, etc.)
- `subject.reference`: `Patient/{PatientID}`
- `encounter.reference`: `Encounter/{EncounterID}`
- `effectiveDateTime`: When observation was taken
- `valueCodeableConcept`: Observation value
- `interpretation[]`: Normal, Abnormal, etc.

**Count**: 43 observations (3-6 per patient)

**Types**: Blood Pressure, Heart Rate, Temperature, Glucose, RBC Count

---

### 9. Condition Resources (`conditionss.json`)

**Structure**: FHIR Bundle with entries

**Key Fields:**
- `resourceType`: "Bundle"
- `type`: "searchset"
- `entry[].resource.resourceType`: "Condition"
- `entry[].resource.id`: Generated ID (eCond...)
- `entry[].resource.clinicalStatus`: active, recurrence, remission, inactive
- `entry[].resource.verificationStatus`: confirmed, unconfirmed
- `entry[].resource.category[]`: Problem List Item, Encounter Diagnosis
- `entry[].resource.code`: ICD-10, SNOMED, ICD-9 codings
- `entry[].resource.subject.reference`: `Patient/{PatientID}`
- `entry[].resource.onsetDateTime`: Onset date
- `entry[].resource.recordedDate`: Recorded date
- `entry[].resource.note[]`: Clinical notes (optional)

**Count**: 32 conditions (2-5 per patient)

**Types**: Hypertension, Diabetes, Osteoporosis, COPD, Anxiety, Depression, etc.

---

### 10. DocumentReference Resources (`docref.json`)

**Structure**: Array of DocumentReference resources

**Key Fields:**
- `resourceType`: "DocumentReference"
- `id`: Generated ID (eDocRef...)
- `status`: current, superseded, entered-in-error
- `docStatus`: final, preliminary, amended
- `type`: Progress Notes, Discharge Summary, Lab Results, Imaging Report
- `category[]`: Clinical Note, Lab Report, Imaging Report
- `subject.reference`: `Patient/{PatientID}`
- `date`: Document date
- `author[]`: Practitioner references
- `authenticator`: Authentication info
- `content[].attachment.url`: `Binary/{BinaryID}`

**Count**: 33 document references (2-5 per patient)

---

### 11. Consent Resources (`consent.json`)

**Structure**: FHIR Bundle with entries

**Key Fields:**
- `resourceType`: "Bundle"
- `type`: "searchset"
- `entry[].resource.resourceType`: "Consent"
- `entry[].resource.id`: Generated ID (eConsent...)
- `entry[].resource.status`: draft, active, inactive, rejected
- `entry[].resource.scope`: Consent Form, Power of Attorney, HIPAA Notice, etc.
- `entry[].resource.category[]`: Consent categories
- `entry[].resource.patient.reference`: `Patient/{PatientID}`
- `entry[].resource.dateTime`: Consent date
- `entry[].resource.provision`: Optional encounter references

**Count**: 31 consents (2-4 per patient)

**Types**: Consent Form, Power of Attorney, HIPAA Notice of Privacy, Advanced Directive, Research Consent

---

### 12. Binary Resources (`binary.json`)

**Structure**: Array of Binary resources

**Key Fields:**
- `resourceType`: "Binary"
- `id`: Generated ID (eBinary...)
- `contentType`: text/rtf, text/html, application/pdf, application/xml, text/plain
- `data`: Base64-encoded synthetic content

**Count**: 46 binary resources

**Referenced By**: DocumentReference resources

---

### 13. Appointment Resources (`appointments.json`)

**Structure**: Bundle with appointments array

**Key Fields:**
- `resourceType`: "Bundle"
- `total`: Number of appointments
- `appointments[]`: Appointment objects
- `appointments[].participants[]`: Patient and provider references

**Count**: 10 appointments

---

### 14. ExplanationOfBenefit Resources (`eob.json`)

**Structure**: FHIR Bundle with OperationOutcome

**Key Fields:**
- `resourceType`: "Bundle"
- `type`: "searchset"
- `total`: 0
- `entry[].resource.resourceType`: "OperationOutcome"
- `entry[].resource.issue[]`: Warning messages indicating no results

**Count**: 0 (empty bundle with OperationOutcome warning)

**Note**: Returns OperationOutcome indicating no EOB resources available (simulating authorization restrictions)

---

### 15. Provenance Resources (`provenance.json`)

**Structure**: Array of Provenance resources

**Key Fields:**
- `resourceType`: "Provenance"
- `id`: Generated ID (eProv...)
- `target[]`: Reference to target resource (Patient, Condition, Procedure, Observation)
- `recorded`: Timestamp when provenance was recorded
- `agent[]`: Agent information
  - `agent[].type`: Author, Enterer, Verifier, Transmitter
  - `agent[].who.reference`: `Practitioner/{PractitionerID}`
  - `agent[].onBehalfOf.display`: Organization name

**Count**: 30 provenance resources

**Targets**: Patients, Conditions, Procedures, Observations

---

## Data Consistency Rules

### 1. ID Preservation
- ✅ Patient IDs are **never changed** - preserved exactly as provided
- ✅ Organization IDs are **never changed** - preserved exactly as provided
- ✅ All other IDs are generated deterministically using hash functions

### 2. Reference Integrity
- ✅ All `Patient/{PatientID}` references match existing patient IDs
- ✅ All `Organization/{OrgID}` references match existing organization IDs
- ✅ All `Practitioner/{PractitionerID}` references match existing practitioner IDs
- ✅ All `Encounter/{EncounterID}` references match existing encounter IDs
- ✅ All `Binary/{BinaryID}` references match existing binary IDs

### 3. Cross-Resource Consistency
- ✅ Coverage IDs follow pattern: `cov-{PatientID}`
- ✅ Each patient has exactly 1 coverage
- ✅ Each patient has 2-5 conditions
- ✅ Each patient has 2-4 encounters
- ✅ Each patient has 1-3 procedures
- ✅ Each patient has 3-6 observations
- ✅ Each patient has 2-5 document references
- ✅ Each patient has 2-4 consents

### 4. Deterministic Generation
- ✅ Same input (Patient ID, Organization ID) always produces same output
- ✅ Hash-based selection ensures consistency
- ✅ Date ranges are realistic (within 1-5 years for most resources)

### 5. HIPAA Compliance
- ✅ All names are fictional
- ✅ All addresses are fictional
- ✅ All phone numbers are synthetic
- ✅ SSNs start with "9" (synthetic pattern)
- ✅ All dates are in the past
- ✅ No real medical data

---

## Usage in Mock API

### Resource Access Patterns

1. **Patient-centric queries:**
   - `GET /Patient/{PatientID}` → Returns patient resource
   - `GET /Encounter?patient={PatientID}` → Returns encounters for patient
   - `GET /Condition?patient={PatientID}` → Returns conditions for patient
   - `GET /Procedure?patient={PatientID}` → Returns procedures for patient
   - `GET /Observation?patient={PatientID}` → Returns observations for patient

2. **Organization-centric queries:**
   - `GET /Organization/{OrgID}` → Returns organization resource
   - `GET /Encounter?organization={OrgID}` → Returns encounters at organization

3. **Practitioner-centric queries:**
   - `GET /Practitioner/{PractitionerID}` → Returns practitioner resource
   - `GET /PractitionerRole?practitioner={PractitionerID}` → Returns roles for practitioner

4. **Document queries:**
   - `GET /DocumentReference?patient={PatientID}` → Returns documents for patient
   - `GET /Binary/{BinaryID}` → Returns binary content

---

## File Structure

```
Sythetic_Data/
├── patients.json              (10 patients)
├── organisation.json          (10 organizations)
├── coverage.json              (10 coverages)
├── practitioner.json          (10 practitioners)
├── practitonerrole.json       (15 practitioner roles)
├── encounterr.json            (31 encounters - Bundle)
├── procedure.json             (20 procedures - Bundle)
├── observation.json           (43 observations)
├── conditionss.json           (32 conditions - Bundle)
├── docref.json                (33 document references)
├── consent.json               (31 consents - Bundle)
├── binary.json                (46 binary resources)
├── appointments.json          (10 appointments - Bundle)
├── eob.json                   (0 EOBs - Bundle with OperationOutcome)
├── provenance.json            (30 provenance resources)
└── DATA_DOCUMENTATION.md      (This file)
```

---

## Generation Scripts

1. **`generate_synthetic_data.py`**: Generates patients, organizations, and coverage
2. **`generate_conditions.py`**: Generates condition resources
3. **`generate_consent_binary_docref.py`**: Generates consent, binary, and document reference resources
4. **`generate_remaining_resources.py`**: Generates encounter, procedure, observation, practitioner, practitionerrole, provenance, and EOB resources

---

## Validation

All resources have been validated for:
- ✅ Valid JSON syntax
- ✅ FHIR R4 structure compliance
- ✅ Cross-resource reference integrity
- ✅ Required field presence
- ✅ Data type correctness
- ✅ Date format compliance (ISO 8601)

---

## Notes

- All dates are in the past (1 month to 5 years ago)
- All identifiers are synthetic and follow FHIR conventions
- Bundle resources include proper `link`, `fullUrl`, and `search` metadata
- Empty resources (EOB) return OperationOutcome with appropriate warnings
- Provenance resources provide audit trail for key resources

---

**Last Updated**: 2025-01-XX  
**Maintainer**: Synthetic Data Generation System

