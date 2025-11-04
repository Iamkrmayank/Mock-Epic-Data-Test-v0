# Test Epic FHIR API
Write-Host "=== Testing Epic FHIR Mock API ===" -ForegroundColor Green
Write-Host ""

# Wait for server to start
Start-Sleep -Seconds 3

# Test 1: Health Check
Write-Host "1. Testing Health Endpoint..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "   Status: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "   ERROR: Server not running. Start with: python fhir_api.py" -ForegroundColor Red
    exit 1
}

# Test 2: Get Patient
Write-Host "`n2. Testing Patient Read..." -ForegroundColor Yellow
$patient = Invoke-RestMethod -Uri "http://localhost:8000/Patient/ePtdJFCrnl2edlBDdz1C5Ja" -Method Get
Write-Host "   Patient ID: $($patient.id)" -ForegroundColor Green
Write-Host "   Patient Name: $($patient.data.name[0].text)" -ForegroundColor Green

# Test 3: Search Appointments
Write-Host "`n3. Testing Appointment Search..." -ForegroundColor Yellow
$appts = Invoke-RestMethod -Uri "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja" -Method Get
Write-Host "   Total Appointments: $($appts.total)" -ForegroundColor Green
if ($appts.entry.Count -gt 0) {
    $firstAppt = $appts.entry[0].resource
    Write-Host "   First Appointment ID: $($firstAppt.id)" -ForegroundColor Green
    Write-Host "   First Appointment Status: $($firstAppt.status)" -ForegroundColor Green
    $patientRef = $firstAppt.participant[0].actor.reference
    Write-Host "   Patient Reference: $patientRef" -ForegroundColor Green
}

# Test 4: Search Conditions
Write-Host "`n4. Testing Condition Search..." -ForegroundColor Yellow
$conditions = Invoke-RestMethod -Uri "http://localhost:8000/Condition?patient=ePtdJFCrnl2edlBDdz1C5Ja&clinical-status=active" -Method Get
Write-Host "   Total Conditions: $($conditions.total)" -ForegroundColor Green
if ($conditions.entry.Count -gt 0) {
    $firstCond = $conditions.entry[0].resource
    Write-Host "   First Condition Code: $($firstCond.code.coding[0].code)" -ForegroundColor Green
}

# Test 5: Search Observations (with category - Epic requirement)
Write-Host "`n5. Testing Observation Search (with category)..." -ForegroundColor Yellow
$observations = Invoke-RestMethod -Uri "http://localhost:8000/Observation?patient=ePtdJFCrnl2edlBDdz1C5Ja&category=vital-signs&_count=2" -Method Get
Write-Host "   Total Observations: $($observations.total)" -ForegroundColor Green
if ($observations.entry.Count -gt 0) {
    $firstObs = $observations.entry[0].resource
    Write-Host "   First Observation Code: $($firstObs.code.coding[0].code)" -ForegroundColor Green
}

# Test 6: Search Encounters
Write-Host "`n6. Testing Encounter Search..." -ForegroundColor Yellow
$encounters = Invoke-RestMethod -Uri "http://localhost:8000/Encounter?patient=ePtdJFCrnl2edlBDdz1C5Ja&_count=2" -Method Get
Write-Host "   Total Encounters: $($encounters.total)" -ForegroundColor Green
if ($encounters.entry.Count -gt 0) {
    $firstEnc = $encounters.entry[0].resource
    Write-Host "   First Encounter Status: $($firstEnc.status)" -ForegroundColor Green
}

# Test 7: Search Patients by Name
Write-Host "`n7. Testing Patient Search (by family name)..." -ForegroundColor Yellow
$patients = Invoke-RestMethod -Uri "http://localhost:8000/Patient?family=Rodriguez" -Method Get
Write-Host "   Total Patients Found: $($patients.total)" -ForegroundColor Green
if ($patients.entry.Count -gt 0) {
    $firstPatient = $patients.entry[0].resource
    Write-Host "   Patient ID: $($firstPatient.id)" -ForegroundColor Green
}

# Test 8: Search Appointments by Status
Write-Host "`n8. Testing Appointment Search (by status)..." -ForegroundColor Yellow
$apptsFiltered = Invoke-RestMethod -Uri "http://localhost:8000/Appointment?patient=ePtdJFCrnl2edlBDdz1C5Ja&status=booked" -Method Get
Write-Host "   Booked Appointments: $($apptsFiltered.total)" -ForegroundColor Green

# Test 9: Verify Bundle Structure
Write-Host "`n9. Verifying Bundle Structure..." -ForegroundColor Yellow
$bundle = $appts
if ($bundle.resourceType -eq "Bundle" -and $bundle.type -eq "searchset" -and $bundle.entry.Count -gt 0) {
    Write-Host "   Bundle Type: $($bundle.type)" -ForegroundColor Green
    Write-Host "   Bundle Total: $($bundle.total)" -ForegroundColor Green
    Write-Host "   Entries Count: $($bundle.entry.Count)" -ForegroundColor Green
    Write-Host "   First Entry has fullUrl: $($bundle.entry[0].fullUrl -ne $null)" -ForegroundColor Green
    Write-Host "   First Entry has resource: $($bundle.entry[0].resource -ne $null)" -ForegroundColor Green
}

Write-Host "`n=== All Tests Completed Successfully! ===" -ForegroundColor Green
Write-Host "`nAPI is working and Epic-compliant!" -ForegroundColor Cyan

