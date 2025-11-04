/**
 * Swagger/OpenAPI documentation setup
 */

import swaggerJsdoc from 'swagger-jsdoc';

const options: swaggerJsdoc.Options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Gooclaim Mock (Epic) FHIR API',
      version: '1.0.0',
      description: 'Mock FHIR API server using Epic-style fixtures',
    },
    servers: [
      {
        url: `http://localhost:${process.env.PORT || 8080}`,
        description: 'Development server',
      },
      {
        url: '/',
        description: 'Current server',
      },
    ],
    tags: [
      { name: 'Patient', description: 'Patient resources' },
      { name: 'Coverage', description: 'Coverage resources' },
      { name: 'Encounter', description: 'Encounter resources' },
      { name: 'Appointment', description: 'Appointment resources' },
      { name: 'Contract', description: 'Contract resources' },
      { name: 'Consent', description: 'Consent resources' },
      { name: 'DocumentReference', description: 'DocumentReference resources' },
      { name: 'Observation', description: 'Observation resources' },
      { name: 'Procedure', description: 'Procedure resources' },
      { name: 'Condition', description: 'Condition resources' },
      { name: 'Organization', description: 'Organization resources' },
      { name: 'Practitioner', description: 'Practitioner resources' },
      { name: 'PractitionerRole', description: 'PractitionerRole resources' },
      { name: 'ExplanationOfBenefit', description: 'ExplanationOfBenefit resources' },
      { name: 'Binary', description: 'Binary resources' },
      { name: 'Provenance', description: 'Provenance resources' },
      { name: 'System', description: 'System endpoints' },
    ],
    paths: {
      '/{resourceType}': {
        get: {
          summary: 'Search resources',
          description: 'Search for resources by type. Returns a Bundle.',
          tags: ['Patient', 'Coverage', 'Encounter', 'Appointment'],
          parameters: [
            {
              name: 'resourceType',
              in: 'path',
              required: true,
              description: 'The FHIR resource type',
              schema: {
                type: 'string',
                enum: [
                  'Patient',
                  'Coverage',
                  'Encounter',
                  'Appointment',
                  'Contract',
                  'Consent',
                  'DocumentReference',
                  'Observation',
                  'Procedure',
                  'Condition',
                  'Organization',
                  'Practitioner',
                  'PractitionerRole',
                  'ExplanationOfBenefit',
                  'Binary',
                  'Provenance',
                ],
              },
            },
            {
              name: '_count',
              in: 'query',
              description: 'Maximum number of results',
              schema: { type: 'integer' },
            },
          ],
          responses: {
            '200': {
              description: 'Successful response - returns Bundle',
              content: {
                'application/fhir+json': {
                  schema: {
                    $ref: '#/components/schemas/Bundle',
                  },
                },
              },
            },
          },
        },
      },
      '/{resourceType}/{id}': {
        get: {
          summary: 'Get resource by ID',
          description: 'Retrieve a specific resource by its ID.',
          tags: ['Patient', 'Coverage', 'Encounter', 'Appointment'],
          parameters: [
            {
              name: 'resourceType',
              in: 'path',
              required: true,
              schema: { type: 'string' },
            },
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: { type: 'string' },
            },
          ],
          responses: {
            '200': {
              description: 'Resource found',
              content: {
                'application/fhir+json': {
                  schema: {
                    type: 'object',
                  },
                },
              },
            },
            '404': {
              description: 'Resource not found',
              content: {
                'application/fhir+json': {
                  schema: {
                    $ref: '#/components/schemas/OperationOutcome',
                  },
                },
              },
            },
          },
        },
      },
      '/Binary/{id}/$content': {
        get: {
          summary: 'Get Binary content',
          description: 'Retrieve binary content as raw bytes.',
          tags: ['Binary'],
          parameters: [
            {
              name: 'id',
              in: 'path',
              required: true,
              schema: { type: 'string' },
            },
          ],
          responses: {
            '200': {
              description: 'Binary content',
              content: {
                'application/octet-stream': {
                  schema: { type: 'string', format: 'binary' },
                },
              },
            },
          },
        },
      },
      '/healthz': {
        get: {
          summary: 'Health check',
          description: 'Returns health status',
          tags: ['System'],
          responses: {
            '200': {
              description: 'Service is healthy',
              content: {
                'application/json': {
                  schema: {
                    type: 'object',
                    properties: {
                      ok: { type: 'boolean' },
                    },
                  },
                },
              },
            },
          },
        },
      },
    },
    components: {
      schemas: {
        Bundle: {
          type: 'object',
          properties: {
            resourceType: { type: 'string', example: 'Bundle' },
            type: { type: 'string', example: 'searchset' },
            total: { type: 'integer' },
            entry: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  resource: { type: 'object' },
                },
              },
            },
          },
        },
        OperationOutcome: {
          type: 'object',
          properties: {
            resourceType: { type: 'string', example: 'OperationOutcome' },
            issue: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  severity: { type: 'string' },
                  code: { type: 'string' },
                  details: {
                    type: 'object',
                    properties: {
                      text: { type: 'string' },
                    },
                  },
                },
              },
            },
          },
        },
      },
    },
  },
  apis: ['./src/**/*.ts'],
};

export const swaggerSpec = swaggerJsdoc(options);

