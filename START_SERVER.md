# How to Start and Test the Epic FHIR API

## Step 1: Start the Server

Open a terminal and run:

```bash
python fhir_api.py
```

Or using uvicorn directly:

```bash
uvicorn fhir_api:app --reload --port 8000
```

The server will start on: `http://localhost:8000`

## Step 2: Test the API

### Option A: Using Python Test Script

In a **new terminal window**, run:

```bash
python test_api.py
```

### Option B: Manual Testing with Browser

Open your browser and visit:

1. **Health Check**: http://localhost:8000/health
2. **Get Patient**: http://localhost:8000/Patient/ePtdJFCrnl2edlBDdz1C5Ja
3. **Search Appointments**: http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja
4. **Search Conditions**: http://localhost:8000/Condition?patient=ePtdJFCrnl2edlBDdz1C5Ja&clinical-status=active
5. **Search Observations**: http://localhost:8000/Observation?patient=ePtdJFCrnl2edlBDdz1C5Ja&category=vital-signs

### Option C: Using PowerShell (Windows)

```powershell
# Test Health
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get

# Test Patient
Invoke-RestMethod -Uri "http://localhost:8000/Patient/ePtdJFCrnl2edlBDdz1C5Ja" -Method Get

# Test Appointments
Invoke-RestMethod -Uri "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja" -Method Get
```

### Option D: Using curl (if available)

```bash
curl http://localhost:8000/health
curl http://localhost:8000/Patient/ePtdJFCrnl2edlBDdz1C5Ja
curl "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja"
```

## Step 3: View API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Expected Test Results

When you run `python test_api.py`, you should see:

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

... (all tests should pass)

[SUCCESS] All tests passed! API is Epic-compliant!
```

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Make sure all dependencies are installed: `pip install -r requirements.txt`

### Connection errors
- Make sure the server is running in a separate terminal
- Wait 2-3 seconds after starting the server before running tests

### Test failures
- Check that all data files exist in `Sythetic_Data/` folder
- Verify the server logs for any errors

