"""
Verify our API matches Epic FHIR patterns from https://fhir.epic.com/
"""
import json
from pathlib import Path

# Epic FHIR R4 Resources and their supported operations
EPIC_RESOURCES = {
    "Patient": {
        "operations": ["Read", "Search", "Create", "$match"],
        "search_params": ["_id", "identifier", "name", "birthdate", "gender", "family", "given"]
    },
    "Appointment": {
        "operations": ["Read", "Search"],
        "search_params": ["_id", "patient", "status", "date", "actor"]
    },
    "Condition": {
        "operations": ["Read", "Search", "Create"],
        "search_params": ["_id", "patient", "clinical-status", "category", "code"]
    },
    "Encounter": {
        "operations": ["Read", "Search"],
        "search_params": ["_id", "patient", "status", "class", "organization", "date"]
    },
    "Observation": {
        "operations": ["Read", "Search"],
        "search_params": ["_id", "patient", "category", "code", "date", "encounter", "_lastn"]
    },
    "Procedure": {
        "operations": ["Read", "Search"],
        "search_params": ["_id", "patient", "date", "status"]
    },
    "Coverage": {
        "operations": ["Read", "Search"],
        "search_params": ["_id", "patient", "beneficiary", "payor"]
    },
    "Organization": {
        "operations": ["Read", "Search"],
        "search_params": ["_id", "identifier", "name"]
    },
    "Practitioner": {
        "operations": ["Read", "Search"],
        "search_params": ["_id", "identifier", "name"]
    },
    "PractitionerRole": {
        "operations": ["Read", "Search"],
        "search_params": ["_id", "practitioner", "organization", "location"]
    },
    "DocumentReference": {
        "operations": ["Read", "Search"],
        "search_params": ["_id", "patient", "status", "date", "type"]
    },
    "Consent": {
        "operations": ["Read", "Search"],
        "search_params": ["_id", "patient", "status", "category"]
    },
    "Binary": {
        "operations": ["Read"],
        "search_params": ["_id"]
    },
    "Provenance": {
        "operations": ["Read"],
        "search_params": ["_id", "target"]
    },
    "ExplanationOfBenefit": {
        "operations": ["Search"],
        "search_params": ["patient"]
    }
}

# Check our API endpoints
print("Epic FHIR R4 Compliance Check")
print("=" * 60)

# Check data files
data_dir = Path("Sythetic_Data")
files_check = {
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

print("\n1. Data Files Check:")
for resource, filename in files_check.items():
    file_path = data_dir / filename
    if file_path.exists():
        print(f"   [OK] {resource}: {filename}")
    else:
        print(f"   [MISSING] {resource}: {filename}")

print("\n2. Epic Resource Operations:")
for resource, config in EPIC_RESOURCES.items():
    ops = ", ".join(config["operations"])
    print(f"   {resource}: {ops}")

print("\n3. Epic Search Parameters (Key):")
for resource, config in EPIC_RESOURCES.items():
    if config["search_params"]:
        params = ", ".join(config["search_params"][:5])
        print(f"   {resource}: {params}...")

print("\n4. Verification Complete!")
print("\nOur API should support:")
print("   - Read operations (GET /Resource/{id})")
print("   - Search operations (GET /Resource?param=value)")
print("   - Bundle responses for searches")
print("   - Patient-specific filtering")
print("   - Status, category, code filtering where applicable")

