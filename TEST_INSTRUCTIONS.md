# 🧪 Testing Instructions

## Quick Start

### Step 1: Start the Server

Open **Terminal 1** and run:

```bash
python fhir_api.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Run Tests

Open **Terminal 2** (keep Terminal 1 running) and run:

```bash
python test_api.py
```

## Expected Test Results

You should see all tests passing:

```
============================================================
Epic FHIR Mock API - Test Suite
============================================================

1. Health Check...
   [OK] Status: 200

2. Get Patient by ID...
   [OK] Resource Type: Patient
   [OK] Resource ID: ePtdJFCrnl2edlBDdz1C5Ja

3. Search Appointments (by patient)...
   [OK] Bundle Type: searchset
   [OK] Total: 10
   [OK] Entries: 10
   [OK] First Entry has fullUrl: True
   [OK] First Entry has resource: True

4. Search Appointments (by status)...
   [OK] Bundle Type: searchset
   [OK] Total: X
   [OK] Entries: X

... (continues for all 10 tests)

============================================================
Test Summary
============================================================
[PASS]: Health Check
[PASS]: Patient Read
[PASS]: Appointment Search
[PASS]: Appointment Status Filter
[PASS]: Condition Search
[PASS]: Observation Search
[PASS]: Encounter Search
[PASS]: Patient Search
[PASS]: Procedure Search
[PASS]: Organization Read

Total: 10/10 tests passed

[SUCCESS] All tests passed! API is Epic-compliant!
```

## Alternative: Browser Testing

Once server is running, open these URLs:

1. **API Docs**: http://localhost:8000/docs
2. **Health**: http://localhost:8000/health
3. **Patient**: http://localhost:8000/Patient/ePtdJFCrnl2edlBDdz1C5Ja
4. **Appointments**: http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja
5. **Conditions**: http://localhost:8000/Condition?patient=ePtdJFCrnl2edlBDdz1C5Ja&clinical-status=active
6. **Observations**: http://localhost:8000/Observation?patient=ePtdJFCrnl2edlBDdz1C5Ja&category=vital-signs

## Test Endpoints Summary

### ✅ Read Operations (Individual Resources)
- `GET /Patient/{id}`
- `GET /Appointment/{id}`
- `GET /Organization/{id}`
- `GET /Condition/{id}`
- `GET /Encounter/{id}`
- `GET /Observation/{id}`
- `GET /Procedure/{id}`

### ✅ Search Operations (Bundle Responses)
- `GET /Patient?family=Rodriguez`
- `GET /Appointment?patient={id}&status=booked`
- `GET /Condition?patient={id}&clinical-status=active`
- `GET /Observation?patient={id}&category=vital-signs`
- `GET /Encounter?patient={id}&status=finished`
- `GET /Procedure?patient={id}&status=completed`

## What Gets Tested

1. ✅ **Server Health** - API is running
2. ✅ **Patient Read** - Individual patient retrieval
3. ✅ **Appointment Search** - Search by patient
4. ✅ **Appointment Status Filter** - Filter by status
5. ✅ **Condition Search** - Search with clinical-status
6. ✅ **Observation Search** - Search with category (Epic requirement)
7. ✅ **Encounter Search** - Search by patient
8. ✅ **Patient Search** - Search by family name
9. ✅ **Procedure Search** - Search by patient
10. ✅ **Organization Read** - Individual organization retrieval

## Epic Compliance Verification

All endpoints return:
- ✅ Correct Bundle structure for searches
- ✅ Epic-compatible fullUrl format
- ✅ Proper resource structure
- ✅ Valid cross-references
- ✅ Correct search parameters

## Troubleshooting

**Server won't start?**
- Check if port 8000 is already in use
- Install dependencies: `pip install fastapi uvicorn requests`

**Tests fail?**
- Make sure server is running in Terminal 1
- Wait 2-3 seconds after starting server
- Check that all data files exist in `Sythetic_Data/`

**Connection errors?**
- Verify server is running: http://localhost:8000/health
- Check firewall settings
- Try `127.0.0.1:8000` instead of `localhost:8000`

