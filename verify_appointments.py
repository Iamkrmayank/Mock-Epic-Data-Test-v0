"""Verify appointments have correct patient and organization IDs"""
import json

# Load data
with open("Sythetic_Data/patients.json", "r", encoding="utf-8") as f:
    patients = json.load(f)

with open("Sythetic_Data/organisation.json", "r", encoding="utf-8") as f:
    organizations = json.load(f)

with open("Sythetic_Data/appointments.json", "r", encoding="utf-8") as f:
    appointments_data = json.load(f)

patient_ids = [p["id"] for p in patients]
org_ids = [o["id"] for o in organizations]

# Create patient-org mapping from patient data
patient_org_map = {}
for i, patient in enumerate(patients):
    patient_id = patient["id"]
    managing_org = patient.get("data", {}).get("managingOrganization", {}).get("reference", "")
    if managing_org:
        org_id = managing_org.replace("Organization/", "")
    else:
        org_id = organizations[i % len(organizations)]["id"]
    patient_org_map[patient_id] = org_id

print("Patient-Organization Mapping:")
for pid, oid in patient_org_map.items():
    print(f"  {pid[:30]}... -> {oid[:30]}...")

print("\nVerifying Appointments:")
appointments = appointments_data.get("appointments", [])
all_correct = True

for i, appointment in enumerate(appointments):
    expected_patient_id = patient_ids[i % len(patient_ids)]
    expected_org_id = patient_org_map[expected_patient_id]
    
    if "full_resource" in appointment:
        participants = appointment["full_resource"].get("participant", [])
        patient_ref = None
        location_ref = None
        
        for participant in participants:
            actor = participant.get("actor", {})
            if isinstance(actor, dict):
                ref = actor.get("reference", "")
                if ref.startswith("Patient/"):
                    patient_ref = ref.replace("Patient/", "")
                elif ref.startswith("Location/"):
                    location_ref = ref.replace("Location/", "")
        
        patient_ok = patient_ref == expected_patient_id
        org_ok = location_ref == expected_org_id
        
        status = "OK" if (patient_ok and org_ok) else "ERROR"
        if not (patient_ok and org_ok):
            all_correct = False
        
        print(f"  Appointment {i+1}: {status}")
        print(f"    Patient: {patient_ref[:30]}... (expected: {expected_patient_id[:30]}...) {'[OK]' if patient_ok else '[ERROR]'}")
        print(f"    Location: {location_ref[:30]}... (expected: {expected_org_id[:30]}...) {'[OK]' if org_ok else '[ERROR]'}")

print(f"\n{'All appointments are correctly mapped!' if all_correct else 'Some appointments need fixing!'}")

