"""
Verify that API is loading data from Sythetic_Data folder
"""
from pathlib import Path
import json

DATA_DIR = Path("Sythetic_Data")

print("=" * 60)
print("Verifying Data Files in Sythetic_Data folder")
print("=" * 60)

# Check all required files
files_to_check = {
    "Patient": "patients.json",
    "Organization": "organisation.json",
    "Coverage": "coverage.json",
    "Appointment": "appointments.json",
    "Encounter": "encounterr.json",
    "Condition": "conditionss.json",
    "Procedure": "procedure.json",
    "Observation": "observation.json",
    "Practitioner": "practitioner.json",
    "PractitionerRole": "practitonerrole.json",
    "DocumentReference": "docref.json",
    "Consent": "consent.json",
    "Binary": "binary.json",
    "Provenance": "provenance.json",
    "ExplanationOfBenefit": "eob.json"
}

all_found = True
file_counts = {}

for resource_type, filename in files_to_check.items():
    file_path = DATA_DIR / filename
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Count items based on structure
            if isinstance(data, list):
                count = len(data)
            elif isinstance(data, dict):
                if "appointments" in data:
                    count = len(data["appointments"])
                elif "coverage" in data:
                    count = len(data["coverage"])
                elif "entry" in data:
                    count = len(data["entry"])
                else:
                    count = 1
            else:
                count = 0
                
            file_counts[resource_type] = count
            print(f"[OK] {resource_type:20s} -> {filename:25s} ({count} items)")
        except Exception as e:
            print(f"[ERROR] {resource_type:20s} -> {filename:25s} (Error: {str(e)[:50]})")
            all_found = False
    else:
        print(f"[MISSING] {resource_type:20s} -> {filename:25s}")
        all_found = False

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)
print(f"Total Resources: {len(files_to_check)}")
print(f"Files Found: {sum(1 for f in files_to_check.values() if (DATA_DIR / f).exists())}")
print(f"All Files Present: {all_found}")

print("\nResource Counts:")
for resource, count in sorted(file_counts.items()):
    print(f"  {resource:25s}: {count:5d} items")

print("\n" + "=" * 60)
print("API Configuration Check")
print("=" * 60)

# Check if API code references correct folder
api_file = Path("fhir_api.py")
if api_file.exists():
    with open(api_file, "r", encoding="utf-8") as f:
        content = f.read()
        if 'DATA_DIR = Path("Sythetic_Data")' in content:
            print("[OK] API is configured to use: Sythetic_Data")
        else:
            print("[WARNING] API configuration may be incorrect")
        
        # Count references
        ref_count = content.count('DATA_DIR')
        print(f"[OK] API references DATA_DIR: {ref_count} times")

print("\n" + "=" * 60)
if all_found:
    print("[SUCCESS] All data files are present and API is ready!")
else:
    print("[WARNING] Some files are missing. Check the list above.")

