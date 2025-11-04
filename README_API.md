# GooClaim FHIR Mock API - Epic Compatible

FastAPI service for serving synthetic FHIR R4 test data, fully compatible with Epic FHIR API patterns.

**Reference**: [Epic on FHIR](https://fhir.epic.com/)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure synthetic data files are in `Sythetic_Data/` directory

3. Run the server:
```bash
python fhir_api.py
```

Or with uvicorn directly:
```bash
uvicorn fhir_api:app --reload --port 8000
```

## Epic FHIR Scopes & Resources

According to Epic documentation, this API supports the following scopes and resources:

### Epic Scopes Supported

| Epic Scope | Resource | Operations | Version |
|-----------|----------|------------|---------|
| `system/Patient.read` | Patient | Read, Search | R4 |
| `Appointment.Read (Appointments) (R4)` | Appointment | Read | R4 |
| `Appointment.Search (Appointments) (R4)` | Appointment | Search | R4 |
| `system/Condition.read` | Condition | Read, Search | R4 |
| `system/Encounter.read` | Encounter | Read, Search | R4 |
| `system/Observation.read` | Observation | Read, Search | R4 |
| `system/Procedure.read` | Procedure | Read, Search | R4 |
| `system/Coverage.read` | Coverage | Read, Search | R4 |
| `system/Organization.read` | Organization | Read, Search | R4 |
| `system/Practitioner.read` | Practitioner | Read, Search | R4 |
| `system/PractitionerRole.read` | PractitionerRole | Read, Search | R4 |
| `system/DocumentReference.read` | DocumentReference | Read, Search | R4 |
| `system/Consent.read` | Consent | Read, Search | R4 |
| `system/Binary.read` | Binary | Read | R4 |
| `system/Provenance.read` | Provenance | Read, Search | R4 |
| `system/ExplanationOfBenefit.read` | ExplanationOfBenefit | Search | R4 |

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Available Endpoints

#### Patient Resources
**Epic Scope**: `system/Patient.read`  
**Operations**: Read, Search

- `GET /Patient` - Search all patients
- `GET /Patient/{patient_id}` - Get specific patient

**Epic Search Parameters**:
- `_id` - Patient ID
- `identifier` - Identifier value (MRN, FHIR ID, Insurance Member ID)
- `name` - Full name search
- `family` - Family name
- `given` - Given name
- `birthdate` - Birth date (YYYY-MM-DD)
- `gender` - Gender (male, female, other, unknown)
- `_count` - Number of results

**Example**:
```bash
GET /Patient?family=Rodriguez&gender=female
GET /Patient?identifier=MRN-123456
GET /Patient/{patient_id}
```

#### Appointment Resources
**Epic Scope**: `Appointment.Read (Appointments) (R4)`, `Appointment.Search (Appointments) (R4)`  
**Operations**: Read, Search

- `GET /Appointment` - Search appointments
- `GET /Appointment/{appointment_id}` - Get specific appointment

**Epic Search Parameters**:
- `_id` - Appointment ID
- `patient` - Patient ID (required for patient context)
- `status` - Status (booked, fulfilled, cancelled, noshow)
- `date` - Date filter (Epic standard FHIR format)
- `actor` - Actor reference (Patient/Practitioner/Location)
- `_count` - Number of results

**Epic Date Format** (Standard FHIR):
- `date=eqYYYY-MM-DD` - Exact date
- `date=geYYYY-MM-DD` - On or after date
- `date=leYYYY-MM-DD` - On or before date
- `date=gtYYYY-MM-DD` - After date
- `date=ltYYYY-MM-DD` - Before date
- `date=YYYY-MM-DD` - Partial date matching

**Example**:
```bash
GET /Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&status=booked
GET /Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&date=eq2025-11-05
GET /Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&date=ge2025-01-01&date=le2025-12-31
```

#### Condition Resources
**Epic Scope**: `system/Condition.read`  
**Operations**: Read, Search

- `GET /Condition` - Search conditions
- `GET /Condition/{condition_id}` - Get specific condition

**Epic Search Parameters**:
- `_id` - Condition ID
- `patient` - Patient ID (required for patient context)
- `clinical-status` - Clinical status (active, recurrence, remission, inactive)
- `category` - Category (problem-list-item, encounter-diagnosis)
- `code` - Condition code (ICD-10, SNOMED)
- `_count` - Number of results

**Example**:
```bash
GET /Condition?patient=ePtdJFCrnl2edlBDdz1C5Ja&clinical-status=active
GET /Condition?patient=ePtdJFCrnl2edlBDdz1C5Ja&category=problem-list-item
```

#### Encounter Resources
**Epic Scope**: `system/Encounter.read`  
**Operations**: Read, Search

- `GET /Encounter` - Search encounters
- `GET /Encounter/{encounter_id}` - Get specific encounter

**Epic Search Parameters**:
- `_id` - Encounter ID
- `patient` - Patient ID (required for patient context)
- `organization` - Organization ID
- `status` - Status (planned, arrived, in-progress, finished)
- `class` - Encounter class (AMB, EMER, IMP, OBSENC)
- `date` - Date filter
- `_count` - Number of results

**Example**:
```bash
GET /Encounter?patient=ePtdJFCrnl2edlBDdz1C5Ja&status=finished
GET /Encounter?patient=ePtdJFCrnl2edlBDdz1C5Ja&class=AMB
```

#### Observation Resources
**Epic Scope**: `system/Observation.read`  
**Operations**: Read, Search

- `GET /Observation` - Search observations
- `GET /Observation/{observation_id}` - Get specific observation

**Epic Search Parameters**:
- `_id` - Observation ID
- `patient` - Patient ID (required for patient context)
- `encounter` - Encounter ID
- `category` - Category (required if no code/patient) - vital-signs, laboratory, imaging
- `code` - Observation code (required if no category/patient)
- `date` - Date filter
- `_count` - Number of results

**⚠️ Epic Requirement**: At least one of `category`, `code`, or `patient` must be provided.

**Example**:
```bash
GET /Observation?patient=ePtdJFCrnl2edlBDdz1C5Ja&category=vital-signs
GET /Observation?patient=ePtdJFCrnl2edlBDdz1C5Ja&category=laboratory
GET /Observation?code=85354-9&patient=ePtdJFCrnl2edlBDdz1C5Ja
```

#### Procedure Resources
**Epic Scope**: `system/Procedure.read`  
**Operations**: Read, Search

- `GET /Procedure` - Search procedures
- `GET /Procedure/{procedure_id}` - Get specific procedure

**Epic Search Parameters**:
- `_id` - Procedure ID
- `patient` - Patient ID (required for patient context)
- `status` - Status (completed, in-progress, not-done)
- `date` - Date filter
- `_count` - Number of results

**Example**:
```bash
GET /Procedure?patient=ePtdJFCrnl2edlBDdz1C5Ja&status=completed
```

#### Coverage Resources
**Epic Scope**: `system/Coverage.read`  
**Operations**: Read, Search

- `GET /Coverage` - Search coverages
- `GET /Coverage/{coverage_id}` - Get specific coverage

**Epic Search Parameters**:
- `_id` - Coverage ID
- `patient` - Patient ID
- `beneficiary` - Beneficiary ID
- `payor` - Payor organization
- `_count` - Number of results

**Example**:
```bash
GET /Coverage?patient=ePtdJFCrnl2edlBDdz1C5Ja
```

#### Organization Resources
**Epic Scope**: `system/Organization.read`  
**Operations**: Read, Search

- `GET /Organization` - Search organizations
- `GET /Organization/{org_id}` - Get specific organization

**Epic Search Parameters**:
- `_id` - Organization ID
- `identifier` - Identifier value
- `name` - Organization name
- `_count` - Number of results

#### Practitioner Resources
**Epic Scope**: `system/Practitioner.read`  
**Operations**: Read, Search

- `GET /Practitioner` - Search practitioners
- `GET /Practitioner/{practitioner_id}` - Get specific practitioner

**Epic Search Parameters**:
- `_id` - Practitioner ID
- `identifier` - Identifier value
- `name` - Practitioner name
- `_count` - Number of results

#### PractitionerRole Resources
**Epic Scope**: `system/PractitionerRole.read`  
**Operations**: Read, Search

- `GET /PractitionerRole` - Search practitioner roles
- `GET /PractitionerRole/{role_id}` - Get specific role

**Epic Search Parameters**:
- `_id` - PractitionerRole ID
- `practitioner` - Practitioner ID
- `organization` - Organization ID
- `location` - Location ID
- `_count` - Number of results

#### DocumentReference Resources
**Epic Scope**: `system/DocumentReference.read`  
**Operations**: Read, Search

- `GET /DocumentReference` - Search documents
- `GET /DocumentReference/{doc_id}` - Get specific document

**Epic Search Parameters**:
- `_id` - DocumentReference ID
- `patient` - Patient ID (required for patient context)
- `status` - Status (current, superseded, entered-in-error)
- `date` - Date filter
- `type` - Document type
- `_count` - Number of results

#### Consent Resources
**Epic Scope**: `system/Consent.read`  
**Operations**: Read, Search

- `GET /Consent` - Search consents
- `GET /Consent/{consent_id}` - Get specific consent

**Epic Search Parameters**:
- `_id` - Consent ID
- `patient` - Patient ID (required for patient context)
- `status` - Status (draft, active, inactive, rejected)
- `category` - Category code
- `_count` - Number of results

#### Binary Resources
**Epic Scope**: `system/Binary.read`  
**Operations**: Read

- `GET /Binary/{binary_id}` - Get specific binary resource

#### Provenance Resources
**Epic Scope**: `system/Provenance.read`  
**Operations**: Read, Search

- `GET /Provenance` - Search provenance
- `GET /Provenance/{provenance_id}` - Get specific provenance

**Epic Search Parameters**:
- `_id` - Provenance ID
- `target` - Target resource reference
- `_count` - Number of results

#### ExplanationOfBenefit
**Epic Scope**: `system/ExplanationOfBenefit.read`  
**Operations**: Search

- `GET /ExplanationOfBenefit` - Returns OperationOutcome (empty results)

## Response Format

All search endpoints return FHIR Bundle format matching Epic:

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 10,
  "link": [{
    "relation": "self",
    "url": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/{Resource}?_count=100"
  }],
  "entry": [
    {
      "fullUrl": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/{Resource}/{id}",
      "resource": {...},
      "search": {"mode": "match"}
    }
  ]
}
```

Individual resource endpoints return the resource directly.

## Example Requests

### Get a specific patient:
```bash
curl http://localhost:8000/Patient/ePtdJFCrnl2edlBDdz1C5Ja
```

### Search appointments for a patient:
```bash
curl "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja"
```

### Search appointments by date (Epic standard):
```bash
# Today's appointments (use actual date)
curl "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&date=eq2025-11-05"

# Date range
curl "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&date=ge2025-01-01&date=le2025-12-31"
```

### Search conditions for a patient:
```bash
curl "http://localhost:8000/Condition?patient=ePtdJFCrnl2edlBDdz1C5Ja&clinical-status=active"
```

### Search observations for a patient (Epic requires category):
```bash
curl "http://localhost:8000/Observation?patient=ePtdJFCrnl2edlBDdz1C5Ja&category=vital-signs"
```

### Get all patients (limited):
```bash
curl "http://localhost:8000/Patient?_count=5"
```

### Health check:
```bash
curl http://localhost:8000/health
```

## Test Patient IDs

Use these patient IDs for testing:
- `ePtdJFCrnl2edlBDdz1C5Ja`
- `ePt2RJtBRnlWmTSHf6pWkLUy`
- `ePtfDLkDmWJ6UuVTAIjvFu7`
- `ePtICPhDeOZIiBOB-Y6sHrFH2ZUC`
- `ePt-lgotu2iXW7GboIRoL3u6`

## Epic Compatibility

✅ All endpoints match Epic FHIR R4 patterns  
✅ All search parameters match Epic documentation  
✅ Response formats match Epic structure  
✅ Bundle URLs match Epic format  
✅ Date filtering uses Epic standard FHIR format  

**Reference**: [Epic on FHIR Documentation](https://fhir.epic.com/)

## Notes

- This is a mock API for testing purposes
- All data is synthetic and HIPAA-safe
- Security features (OAuth 2.0) will be added in production
- Date format: Use Epic standard FHIR prefixes (eq, ge, le, gt, lt)
