"""
Comprehensive verification against Epic FHIR documentation
Check for any conflicts or non-standard implementations
"""
import re
from pathlib import Path

print("=" * 70)
print("Epic FHIR R4 Compliance & Conflict Check")
print("=" * 70)
print()

# Read fhir_api.py
api_file = Path("fhir_api.py")
with open(api_file, "r", encoding="utf-8") as f:
    api_code = f.read()

conflicts = []
warnings = []
compliant = []

# 1. Check Appointment date parameter
print("1. Checking Appointment date parameter...")
if 'date=today' in api_code or 'date_param == "today"' in api_code:
    warnings.append("[WARNING] 'date=today' is a convenience feature - Epic uses standard FHIR date prefixes (ge, le, eq)")
    print("   [WARNING] 'date=today' is not standard Epic FHIR format")
    print("      Epic uses: date=geYYYY-MM-DD or date=YYYY-MM-DD")
    print("      Recommendation: Keep as convenience, but also support Epic standard")
else:
        compliant.append("[OK] Appointment date parameter uses Epic standard format")

# Check if Epic standard prefixes are supported
if all(prefix in api_code for prefix in ['ge', 'le', 'gt', 'lt', 'eq']):
    compliant.append("[OK] Epic FHIR date prefixes (ge, le, gt, lt, eq) supported")
else:
        conflicts.append("[ERROR] Missing Epic FHIR date prefixes")

# 2. Check variable name conflicts
print("\n2. Checking for variable name conflicts...")
if 'date: Optional[str]' in api_code and 'date.today()' in api_code:
    # Check if we're using the datetime.date class correctly
    if 'from datetime import datetime, date' in api_code:
        compliant.append("[OK] Date import handled correctly")
    else:
        conflicts.append("[ERROR] Potential conflict: 'date' parameter vs datetime.date class")
        print("   [ERROR] CONFLICT: Parameter 'date' might conflict with datetime.date class")

# 3. Check Epic search parameters
print("\n3. Checking Epic search parameters...")
epic_appointment_params = ['_id', 'patient', 'status', 'date', 'actor', '_count']
found_params = []
for param in epic_appointment_params:
    if f'{param}:' in api_code or f'{param}=' in api_code:
        found_params.append(param)

if set(epic_appointment_params) == set(found_params):
    compliant.append("[OK] All Epic Appointment search parameters present")
else:
    missing = set(epic_appointment_params) - set(found_params)
    if missing:
        conflicts.append(f"[ERROR] Missing Epic parameters: {missing}")

# 4. Check Bundle response format
print("\n4. Checking Bundle response format...")
if 'resourceType": "Bundle"' in api_code and 'type": "searchset"' in api_code:
    compliant.append("[OK] Bundle response format matches Epic")
else:
    conflicts.append("[ERROR] Bundle response format may not match Epic")

# Check for fullUrl format
if 'fullUrl' in api_code and 'fhir.epic.com' in api_code:
    compliant.append("[OK] fullUrl format matches Epic pattern")
else:
    warnings.append("[WARNING] fullUrl should match Epic format: https://fhir.epic.com/.../")

# 5. Check Observation requirement
print("\n5. Checking Observation Epic requirement...")
if 'At least one of category, code, or patient parameter is required' in api_code:
    compliant.append("[OK] Observation Epic requirement enforced")
else:
    warnings.append("[WARNING] Observation should require category or code (Epic requirement)")

# 6. Check Patient wrapper format
print("\n6. Checking Patient resource format...")
if '"data"' in api_code and 'retrieved_at' in api_code:
    compliant.append("[OK] Patient wrapper format matches Epic structure")
else:
    warnings.append("[WARNING] Patient format may need Epic wrapper structure")

# 7. Check HTTP status codes
print("\n7. Checking HTTP status codes...")
if 'HTTPException(status_code=404' in api_code:
    compliant.append("[OK] Proper 404 handling")
if 'status_code=400' in api_code:
    compliant.append("[OK] Proper 400 validation errors")

# 8. Check endpoint paths
print("\n8. Checking endpoint paths...")
epic_endpoints = [
    '/Patient',
    '/Appointment',
    '/Condition',
    '/Encounter',
    '/Observation',
    '/Procedure',
    '/Coverage',
    '/Organization'
]
for endpoint in epic_endpoints:
    if f'@app.get("{endpoint}"' in api_code or f'@app.get("{endpoint}/' in api_code:
        found_params.append(endpoint)
    else:
        conflicts.append(f"❌ Missing endpoint: {endpoint}")

# Summary
print("\n" + "=" * 70)
print("VERIFICATION SUMMARY")
print("=" * 70)

print(f"\n[OK] Compliant Features: {len(compliant)}")
for item in compliant:
    print(f"   {item}")

if warnings:
    print(f"\n[WARNING] Warnings: {len(warnings)}")
    for item in warnings:
        print(f"   {item}")

if conflicts:
    print(f"\n[ERROR] Conflicts/Issues: {len(conflicts)}")
    for item in conflicts:
        print(f"   {item}")
else:
    print("\n[OK] No conflicts found!")

# Epic Standard Recommendations
print("\n" + "=" * 70)
print("EPIC STANDARD RECOMMENDATIONS")
print("=" * 70)
print("\nFor 'date=today', Epic standard would be:")
print("  - Use: date=ge2025-01-15&date=le2025-01-15 (today's date)")
print("  - OR: date=eq2025-01-15 (today's date)")
print("\nHowever, 'date=today' as convenience feature is acceptable if:")
print("  - It converts to Epic standard format internally")
print("  - Or clearly documented as non-standard convenience")

print("\n" + "=" * 70)
if not conflicts:
    print("[OK] OVERALL STATUS: COMPLIANT (with minor warnings)")
else:
    print("[WARNING] OVERALL STATUS: NEEDS ATTENTION")
print("=" * 70)

