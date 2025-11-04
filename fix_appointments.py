"""
Fix appointments.json to ensure correct patient and organization ID references
"""
import json
from pathlib import Path

# Load data
patients_file = Path("Sythetic_Data/patients.json")
orgs_file = Path("Sythetic_Data/organisation.json")
appointments_file = Path("Sythetic_Data/appointments.json")

with open(patients_file, "r", encoding="utf-8") as f:
    patients = json.load(f)

with open(orgs_file, "r", encoding="utf-8") as f:
    organizations = json.load(f)

with open(appointments_file, "r", encoding="utf-8") as f:
    appointments_data = json.load(f)

# Create mapping of patient IDs to their organization IDs
patient_org_map = {}
for i, patient in enumerate(patients):
    patient_id = patient["id"]
    # Get managing organization from patient data
    managing_org = patient.get("data", {}).get("managingOrganization", {}).get("reference", "")
    if managing_org:
        org_id = managing_org.replace("Organization/", "")
    else:
        # Fallback: use corresponding organization by index
        org_id = organizations[i % len(organizations)]["id"]
    patient_org_map[patient_id] = org_id

print("Patient-Organization Mapping:")
for pid, oid in patient_org_map.items():
    print(f"  Patient {pid[:20]}... -> Org {oid[:20]}...")

# Fix appointments
patient_ids = [p["id"] for p in patients]
org_ids = [o["id"] for o in organizations]

appointments = appointments_data.get("appointments", [])

for i, appointment in enumerate(appointments):
    # Get the correct patient ID for this appointment index
    patient_id = patient_ids[i % len(patient_ids)]
    org_id = patient_org_map[patient_id]
    
    # Update patient reference in full_resource
    if "full_resource" in appointment:
        participants = appointment["full_resource"].get("participant", [])
        for participant in participants:
            actor = participant.get("actor", {})
            if isinstance(actor, dict):
                ref = actor.get("reference", "")
                # Update patient reference
                if ref.startswith("Patient/"):
                    actor["reference"] = f"Patient/{patient_id}"
                    # Update display name from patient data
                    patient_data = next((p for p in patients if p["id"] == patient_id), None)
                    if patient_data:
                        names = patient_data.get("data", {}).get("name", [])
                        if names:
                            name_obj = names[0]
                            given = name_obj.get("given", [])
                            family = name_obj.get("family", "")
                            if given and family:
                                actor["display"] = f"{family}, {given[0]}"
                # Update location reference
                elif ref.startswith("Location/"):
                    actor["reference"] = f"Location/{org_id}"
                    # Keep location display as is (it's just a location name)

print(f"\nFixed {len(appointments)} appointments")

# Save updated appointments
with open(appointments_file, "w", encoding="utf-8") as f:
    json.dump(appointments_data, f, indent=2, ensure_ascii=False)

print(f"Updated appointments saved to {appointments_file}")

# Verify
print("\nVerification:")
for i, appointment in enumerate(appointments):
    patient_id = patient_ids[i % len(patient_ids)]
    if "full_resource" in appointment:
        participants = appointment["full_resource"].get("participant", [])
        for participant in participants:
            actor = participant.get("actor", {})
            if isinstance(actor, dict):
                ref = actor.get("reference", "")
                if ref.startswith("Patient/"):
                    print(f"  Appointment {i+1}: Patient {ref} (expected: Patient/{patient_id})")
                elif ref.startswith("Location/"):
                    expected_org = patient_org_map[patient_id]
                    print(f"  Appointment {i+1}: Location {ref} (expected: Location/{expected_org})")

print("\nDone!")

