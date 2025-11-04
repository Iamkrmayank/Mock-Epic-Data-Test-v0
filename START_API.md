# Quick Start - FHIR Mock API

## Installation

```bash
pip install -r requirements.txt
```

## Run the API

```bash
python fhir_api.py
```

The API will start on: `http://localhost:8000`

## Test the API

### 1. Check Health
```bash
curl http://localhost:8000/health
```

### 2. Get a Specific Patient
```bash
curl http://localhost:8000/Patient/ePtdJFCrnl2edlBDdz1C5Ja
```

### 3. Search Encounters for a Patient
```bash
curl "http://localhost:8000/Encounter?patient=ePtdJFCrnl2edlBDdz1C5Ja"
```

### 4. Search Conditions for a Patient
```bash
curl "http://localhost:8000/Condition?patient=ePtdJFCrnl2edlBDdz1C5Ja"
```

### 5. Search Observations for a Patient
```bash
curl "http://localhost:8000/Observation?patient=ePtdJFCrnl2edlBDdz1C5Ja"
```

### 6. Get All Patients
```bash
curl "http://localhost:8000/Patient?_count=5"
```

## Test Patient IDs

Use these to test patient-specific queries:
- `ePtdJFCrnl2edlBDdz1C5Ja`
- `ePt2RJtBRnlWmTSHf6pWkLUy`
- `ePtfDLkDmWJ6UuVTAIjvFu7`

## Browser Access

Open in browser:
- API Docs (Swagger UI): http://localhost:8000/docs
- Alternative Docs (ReDoc): http://localhost:8000/redoc

## Verify Data is Loading

Run the test script:
```bash
python test_api.py
```

This will verify all data files are accessible and loaded correctly.

