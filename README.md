# GooClaim Epic FHIR Mock Server - R&D Purpose Only

A FastAPI-based **Mock Epic FHIR R4 API Server** that serves synthetic, HIPAA-safe test data for development and testing purposes. This is a **mock implementation** that simulates Epic's FHIR API structure and responses.

## ⚠️ IMPORTANT DISCLAIMERS

### 🔴 This is a MOCK Server - NOT Real Epic Integration

- **This is NOT connected to Epic's real FHIR API**
- **This is NOT Epic's official server**
- **This is a mock/test server using synthetic data**
- **All data is fictional and HIPAA-safe**

### 🎯 Purpose & Usage

**ONLY for GooClaim R&D purposes:**
- Internal development and testing
- API integration testing
- Learning FHIR R4 structure
- Mock data for development environments

**⚠️ DO NOT USE for:**
- Production environments
- Real patient data
- Clinical decision making
- Any commercial purposes outside GooClaim R&D

### 📋 For Other Work

**If you need real Epic FHIR integration:**
1. Register your application at [Epic on FHIR](https://fhir.epic.com/)
2. Follow Epic's official documentation
3. Complete Epic's app registration process
4. Set up proper OAuth2 authentication
5. Use Epic's sandbox for testing
6. **Do NOT use this mock server for production work**

---

## 🚀 Features

- **Epic-Compatible API Structure**: Mimics Epic's FHIR R4 API patterns
- **Synthetic Test Data**: 15 FHIR resources with realistic but fictional data
- **Full Resource Support**: Patient, Appointment, Condition, Encounter, Observation, Procedure, Coverage, and more
- **Epic Standard Search Parameters**: All Epic search parameters supported
- **Bundle Responses**: Returns Epic-compatible FHIR Bundle format
- **HIPAA-Safe**: All data is synthetic and cannot be linked to real patients

## 📋 Requirements

- Python 3.10+
- FastAPI
- Uvicorn

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Iamkrmayank/Mock-Epic-Data-Test-v0.git
   cd Mock-Epic-Data-Test-v0
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify data files exist**:
   ```bash
   # Check that Sythetic_Data folder contains all JSON files
   ls Sythetic_Data/
   ```

## 🏃‍♂️ Running the Mock Server

### Start the Server

```bash
# Option 1: Direct Python
python fhir_api.py

# Option 2: Using Uvicorn
uvicorn fhir_api:app --reload --host 0.0.0.0 --port 8000
```

The server will start on: `http://localhost:8000`

### Verify Server is Running

```bash
# Health check
curl http://localhost:8000/health

# Or visit in browser
http://localhost:8000/health
```

## 🧪 How to Test the API

### 1. Interactive API Documentation

Once the server is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide interactive documentation where you can test all endpoints directly.

### 2. Using cURL

#### Test Health Endpoint
```bash
curl http://localhost:8000/health
```

#### Get a Patient
```bash
curl http://localhost:8000/Patient/ePtdJFCrnl2edlBDdz1C5Ja
```

#### Search Patients
```bash
# By family name
curl "http://localhost:8000/Patient?family=Rodriguez"

# By identifier
curl "http://localhost:8000/Patient?identifier=MRN-77dd3a"
```

#### Get Appointments
```bash
# All appointments for a patient
curl "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja"

# Appointments by status
curl "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&status=booked"

# Appointments by date (Epic standard format)
curl "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&date=eq2025-11-05"
```

#### Get Conditions
```bash
# Active conditions
curl "http://localhost:8000/Condition?patient=ePtdJFCrnl2edlBDdz1C5Ja&clinical-status=active"
```

#### Get Observations (Epic requires category)
```bash
# Vital signs
curl "http://localhost:8000/Observation?patient=ePtdJFCrnl2edlBDdz1C5Ja&category=vital-signs"

# Lab results
curl "http://localhost:8000/Observation?patient=ePtdJFCrnl2edlBDdz1C5Ja&category=laboratory"
```

#### Get Encounters
```bash
curl "http://localhost:8000/Encounter?patient=ePtdJFCrnl2edlBDdz1C5Ja&status=finished"
```

### 3. Using Python Test Script

We provide a test script:

```bash
# Start server in one terminal
python fhir_api.py

# In another terminal, run tests
python test_api.py
```

This will test all major endpoints and verify Epic compatibility.

### 4. Using Browser

Simply visit these URLs in your browser:

- Health: `http://localhost:8000/health`
- Patient: `http://localhost:8000/Patient/ePtdJFCrnl2edlBDdz1C5Ja`
- Appointments: `http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja`
- API Docs: `http://localhost:8000/docs`

### 5. Using PowerShell (Windows)

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get

# Get patient
Invoke-RestMethod -Uri "http://localhost:8000/Patient/ePtdJFCrnl2edlBDdz1C5Ja" -Method Get

# Search appointments
Invoke-RestMethod -Uri "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja" -Method Get
```

## 📚 API Endpoints

### Base URL
```
http://localhost:8000
```

### Available Resources

| Resource | Endpoints | Epic Scope Supported |
|----------|-----------|---------------------|
| **Patient** | `GET /Patient`, `GET /Patient/{id}` | `system/Patient.read` |
| **Appointment** | `GET /Appointment`, `GET /Appointment/{id}` | `Appointment.Read/Search (Appointments) (R4)` |
| **Condition** | `GET /Condition`, `GET /Condition/{id}` | `system/Condition.read` |
| **Encounter** | `GET /Encounter`, `GET /Encounter/{id}` | `system/Encounter.read` |
| **Observation** | `GET /Observation`, `GET /Observation/{id}` | `system/Observation.read` |
| **Procedure** | `GET /Procedure`, `GET /Procedure/{id}` | `system/Procedure.read` |
| **Coverage** | `GET /Coverage`, `GET /Coverage/{id}` | `system/Coverage.read` |
| **Organization** | `GET /Organization`, `GET /Organization/{id}` | `system/Organization.read` |
| **Practitioner** | `GET /Practitioner`, `GET /Practitioner/{id}` | `system/Practitioner.read` |
| **PractitionerRole** | `GET /PractitionerRole`, `GET /PractitionerRole/{id}` | `system/PractitionerRole.read` |
| **DocumentReference** | `GET /DocumentReference`, `GET /DocumentReference/{id}` | `system/DocumentReference.read` |
| **Consent** | `GET /Consent`, `GET /Consent/{id}` | `system/Consent.read` |
| **Binary** | `GET /Binary/{id}` | `system/Binary.read` |
| **Provenance** | `GET /Provenance`, `GET /Provenance/{id}` | `system/Provenance.read` |
| **ExplanationOfBenefit** | `GET /ExplanationOfBenefit` | `system/ExplanationOfBenefit.read` |

## 📖 Epic-Compatible Search Parameters

### Patient
- `_id`, `identifier`, `name`, `family`, `given`, `birthdate`, `gender`, `_count`

### Appointment
- `_id`, `patient`, `status`, `date`, `actor`, `_count`
- **Date Format**: Epic standard FHIR (`eqYYYY-MM-DD`, `geYYYY-MM-DD`, `leYYYY-MM-DD`, `gtYYYY-MM-DD`, `ltYYYY-MM-DD`)

### Condition
- `_id`, `patient`, `clinical-status`, `category`, `code`, `_count`

### Observation
- `_id`, `patient`, `encounter`, `category`, `code`, `date`, `_count`
- **⚠️ Epic Requirement**: Must include `category` or `code` (unless `patient` provided)

### Encounter
- `_id`, `patient`, `organization`, `status`, `class`, `date`, `_count`

For complete parameter documentation, see [README_API.md](README_API.md)

## 📊 Test Patient IDs

Use these synthetic patient IDs for testing:

- `ePtdJFCrnl2edlBDdz1C5Ja`
- `ePt2RJtBRnlWmTSHf6pWkLUy`
- `ePtfDLkDmWJ6UuVTAIjvFu7`
- `ePtICPhDeOZIiBOB-Y6sHrFH2ZUC`
- `ePt-lgotu2iXW7GboIRoL3u6`
- `ePtHwnMztVuaP.coUNEhEk`
- `ePt.iqq8vH2BzNZV45pFCiR`
- `ePtDCajhDieQjEJ.Bq8F80`
- `ePtmm3T207gmhZRnFyy5r2xJ7`
- `ePtj4mgblEv0.9BZhvWaXH6K2`

## 📋 Response Format

All search endpoints return Epic-compatible FHIR Bundle format:

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

## 🏗️ Project Structure

```
Mock-Epic-Data-Test-v0/
├── fhir_api.py              # FastAPI mock server
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── README_API.md           # Complete API documentation
├── Sythetic_Data/          # Synthetic FHIR data files
│   ├── patients.json
│   ├── appointments.json
│   ├── conditionss.json
│   ├── encounterr.json
│   ├── observation.json
│   └── ... (all resources)
├── Schema/                 # Schema definitions
├── test_api.py             # Test script
└── ... (other files)
```

## 🔒 Security & Safety

### Data Safety
- ✅ All data is **synthetic and fictional**
- ✅ No real patient information
- ✅ HIPAA-safe test data
- ✅ Cannot be linked to real individuals

### Usage Warnings
- ⚠️ **This is a MOCK server** - not for production
- ⚠️ **No authentication** - for local testing only
- ⚠️ **Do not expose to public internet** without proper security
- ⚠️ **For GooClaim R&D only** - not for other organizations

### For Production Use
If you need real Epic integration:
1. Register at [Epic on FHIR](https://fhir.epic.com/)
2. Complete Epic's app registration
3. Implement OAuth2 authentication
4. Use Epic's sandbox for testing
5. Follow Epic's security guidelines

## 🚨 Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Verify dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.10+)

### No data returned
- Verify `Sythetic_Data/` folder exists
- Check that JSON files are present
- See server logs for errors

### Test failures
- Make sure server is running: `http://localhost:8000/health`
- Wait 2-3 seconds after starting server
- Check test script output for specific errors

### Connection errors
- Verify server is running
- Check firewall settings
- Try `127.0.0.1:8000` instead of `localhost:8000`

## 📝 Documentation

- [README_API.md](README_API.md) - Complete API documentation with Epic scopes
- [EPIC_COMPLIANCE_CHECK.md](EPIC_COMPLIANCE_CHECK.md) - Epic compliance verification
- [EPIC_FINAL_VERIFICATION.md](EPIC_FINAL_VERIFICATION.md) - Final verification report
- [TEST_INSTRUCTIONS.md](TEST_INSTRUCTIONS.md) - Detailed testing guide

## 🔗 References

- [Epic on FHIR](https://fhir.epic.com/) - Epic's official FHIR documentation
- [FHIR R4 Specification](https://www.hl7.org/fhir/R4/) - HL7 FHIR standard

## ⚖️ Legal & Compliance

### Disclaimer
- This is a **mock/test server** for development purposes only
- **NOT affiliated with Epic Systems Corporation**
- **NOT for production use**
- **GooClaim R&D internal use only**

### For Real Epic Integration
If you require real Epic FHIR integration:
- Register your application properly
- Follow Epic's terms of service
- Comply with HIPAA and healthcare regulations
- Use Epic's official sandbox for testing
- **Do NOT use this mock server**

## 📄 License

This project is for **GooClaim R&D purposes only**. See LICENSE file for details.

---

## 🎯 Quick Start Summary

1. **Install**: `pip install -r requirements.txt`
2. **Run**: `python fhir_api.py`
3. **Test**: Visit `http://localhost:8000/docs`
4. **Verify**: `curl http://localhost:8000/health`

**Remember**: This is a MOCK server with synthetic data - for GooClaim R&D testing only!

---

**⚠️ Important**: This mock server is for internal GooClaim R&D purposes only. For production Epic integration, please set up your own implementation following Epic's official documentation and compliance requirements.
