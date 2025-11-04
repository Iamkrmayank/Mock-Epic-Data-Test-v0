/**
 * FHIR helper functions
 */

export interface FHIRResource {
  resourceType: string;
  id?: string;
  [key: string]: any;
}

export interface FHIRBundle {
  resourceType: "Bundle";
  type: "searchset" | "document" | "message" | "transaction" | "transaction-response" | "batch" | "batch-response" | "history" | "searchset" | "collection";
  total?: number;
  entry?: Array<{
    resource: FHIRResource;
  }>;
}

export interface OperationOutcome {
  resourceType: "OperationOutcome";
  issue: Array<{
    severity: "error" | "warning" | "information";
    code: string;
    details?: {
      text: string;
    };
  }>;
}

/**
 * Wrap a single resource into a Bundle
 */
export function wrapToBundle(resource: FHIRResource): FHIRBundle {
  return {
    resourceType: "Bundle",
    type: "searchset",
    total: 1,
    entry: [{ resource }]
  };
}

/**
 * Create an empty searchset Bundle
 */
export function emptyBundle(): FHIRBundle {
  return {
    resourceType: "Bundle",
    type: "searchset",
    total: 0,
    entry: []
  };
}

/**
 * Create an OperationOutcome for 404
 */
export function operationOutcome404(resourceType: string, id: string): OperationOutcome {
  return {
    resourceType: "OperationOutcome",
    issue: [
      {
        severity: "error",
        code: "not-found",
        details: {
          text: `${resourceType} with id '${id}' not found`
        }
      }
    ]
  };
}

/**
 * Check if a resource is a Bundle
 */
export function isBundle(resource: any): resource is FHIRBundle {
  return resource?.resourceType === "Bundle";
}

