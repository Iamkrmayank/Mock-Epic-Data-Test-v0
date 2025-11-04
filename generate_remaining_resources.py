import json
import hashlib
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set

# Encounter types and classes
ENCOUNTER_CLASSES = [
    {"code": "AMB", "display": "Ambulatory"},
    {"code": "EMER", "display": "Emergency"},
    {"code": "IMP", "display": "Inpatient"},
    {"code": "OBSENC", "display": "Observation"},
    {"code": "AMB", "display": "Outpatient"}
]

ENCOUNTER_TYPES = [
    {"code": "102", "display": "Outpatient", "text": "Outpatient"},
    {"code": "101", "display": "Inpatient", "text": "Inpatient"},
    {"code": "103", "display": "Emergency", "text": "Emergency"},
    {"code": "104", "display": "Urgent Care", "text": "Urgent Care"}
]

ENCOUNTER_STATUSES = ["planned", "arrived", "triaged", "in-progress", "onleave", "finished", "cancelled"]

PARTICIPANT_TYPES = [
    {"code": "ATND", "display": "attender"},
    {"code": "REF", "display": "referrer"},
    {"code": "CON", "display": "consultant"}
]

# Practitioner specialties
PRACTITIONER_SPECIALTIES = [
    {"name": "Cardiology", "code": "207RC0000X", "display": "Cardiologist"},
    {"name": "Internal Medicine", "code": "207RI0001X", "display": "Internal Medicine"},
    {"name": "Family Practice", "code": "208D00000X", "display": "Family Physician"},
    {"name": "Pediatrics", "code": "208000000X", "display": "Pediatrician"},
    {"name": "Orthopedics", "code": "207XX0005X", "display": "Orthopedic Surgeon"},
    {"name": "General Surgery", "code": "208600000X", "display": "Surgeon"}
]

PRACTITIONER_NAMES = [
    ("Smith", "John"), ("Johnson", "Sarah"), ("Williams", "Michael"), ("Brown", "Emily"),
    ("Jones", "David"), ("Garcia", "Maria"), ("Miller", "Robert"), ("Davis", "Jennifer"),
    ("Rodriguez", "James"), ("Martinez", "Patricia")
]

# Procedure types
PROCEDURE_CATEGORIES = [
    {"code": "387713003", "display": "Surgical procedure", "text": "Surgical History"},
    {"code": "103693007", "display": "Diagnostic procedure", "text": "Diagnostic"},
    {"code": "409073007", "display": "Evaluation procedure", "text": "Evaluation"}
]

PROCEDURE_CODES = [
    "CESAREAN SECTION", "APPENDECTOMY", "CHOLECYSTECTOMY", "HYSTERECTOMY",
    "Knee Replacement", "Hip Replacement", "Cataract Surgery", "Angioplasty",
    "Colonoscopy", "Endoscopy", "Cardiac Catheterization", "Mastectomy"
]

PROCEDURE_STATUSES = ["preparation", "in-progress", "not-done", "on-hold", "stopped", "completed", "entered-in-error", "unknown"]

# Observation types
OBSERVATION_CATEGORIES = [
    {"code": "laboratory", "display": "Laboratory", "text": "Laboratory"},
    {"code": "vital-signs", "display": "Vital Signs", "text": "Vital Signs"},
    {"code": "imaging", "display": "Imaging", "text": "Imaging"},
    {"code": "survey", "display": "Survey", "text": "Survey"}
]

OBSERVATION_CODES = [
    {"code": "85354-9", "display": "Blood Pressure", "text": "Blood Pressure"},
    {"code": "8867-4", "display": "Heart Rate", "text": "Heart Rate"},
    {"code": "9279-1", "display": "Respiratory Rate", "text": "Respiratory Rate"},
    {"code": "8310-5", "display": "Body Temperature", "text": "Body Temperature"},
    {"code": "2339-0", "display": "Glucose", "text": "Glucose"},
    {"code": "789-8", "display": "Red Blood Cell Count", "text": "RBC Count"}
]

OBSERVATION_STATUSES = ["registered", "preliminary", "final", "amended", "corrected", "cancelled", "entered-in-error", "unknown"]

# Provenance agent types
PROVENANCE_AGENT_TYPES = [
    {"code": "author", "display": "Author", "text": "Author"},
    {"code": "enterer", "display": "Enterer", "text": "Enterer"},
    {"code": "verifier", "display": "Verifier", "text": "Verifier"},
    {"code": "transmitter", "display": "Transmitter", "text": "Transmitter"}
]

def hash_string(s: str) -> str:
    """Generate hash from string for deterministic selection."""
    return hashlib.md5(s.encode()).hexdigest()

def generate_resource_id(prefix: str, seed: str) -> str:
    """Generate a deterministic resource ID."""
    hash_val = hash_string(seed)
    return f"{prefix}{hash_val[:20]}"

def get_patient_name(patient_data: Dict) -> str:
    """Extract patient name from patient data."""
    if "data" in patient_data and "name" in patient_data["data"]:
        names = patient_data["data"]["name"]
        if names and len(names) > 0:
            name_obj = names[0]
            given = name_obj.get("given", [])
            family = name_obj.get("family", "")
            if given and family:
                return f"{family}, {given[0]}"
    return "Unknown Patient"

def generate_practitioner(practitioner_idx: int) -> Dict:
    """Generate a Practitioner resource."""
    hash_val = hash_string(f"practitioner_{practitioner_idx}")
    last_name, first_name = PRACTITIONER_NAMES[practitioner_idx % len(PRACTITIONER_NAMES)]
    specialty = PRACTITIONER_SPECIALTIES[practitioner_idx % len(PRACTITIONER_SPECIALTIES)]
    
    practitioner_id = generate_resource_id("ePract", f"practitioner_{practitioner_idx}")
    npi = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    
    return {
        "resourceType": "Practitioner",
        "id": practitioner_id,
        "identifier": [
            {
                "use": "usual",
                "type": {"text": "NPI"},
                "system": "http://hl7.org/fhir/sid/us-npi",
                "value": npi
            },
            {
                "use": "usual",
                "type": {"text": "PROVID"},
                "system": "urn:oid:1.2.840.114350.1.13.0.1.7.5.737384.6",
                "value": str(1000 + practitioner_idx)
            }
        ],
        "active": True,
        "name": [{
            "use": "usual",
            "text": f"{first_name} {last_name}, MD",
            "family": last_name,
            "given": [first_name, specialty["name"][:3]]
        }],
        "qualification": [{
            "code": {
                "coding": [{
                    "system": "urn:oid:1.2.840.114350.1.13.0.1.7.4.836982.6000",
                    "code": "11",
                    "display": "MD"
                }],
                "text": "MD"
            }
        }]
    }

def generate_practitioner_role(practitioner_id: str, practitioner_name: str, org_id: str, role_idx: int) -> Dict:
    """Generate a PractitionerRole resource."""
    hash_val = hash_string(f"{practitioner_id}_role_{role_idx}")
    specialty = PRACTITIONER_SPECIALTIES[role_idx % len(PRACTITIONER_SPECIALTIES)]
    
    role_id = generate_resource_id("ePractRole", f"{practitioner_id}_{role_idx}")
    
    return {
        "resourceType": "PractitionerRole",
        "id": role_id,
        "active": True,
        "practitioner": {
            "reference": f"Practitioner/{practitioner_id}",
            "display": practitioner_name
        },
        "code": [{
            "coding": [
                {
                    "system": "urn:oid:1.2.840.114350.1.13.861.1.7.10.836982.1040",
                    "code": str(10 + role_idx),
                    "display": specialty["display"]
                },
                {
                    "system": "http://snomed.info/sct",
                    "code": "106289002",
                    "display": specialty["display"]
                }
            ],
            "text": specialty["display"]
        }],
        "specialty": [{
            "coding": [{
                "system": "urn:oid:1.2.840.114350.1.72.1.7.7.10.688867.4160",
                "code": str(10 + role_idx),
                "display": specialty["name"]
            }],
            "text": specialty["name"]
        }],
        "location": [{
            "reference": f"Location/{org_id}"
        }],
        "telecom": [{
            "system": "phone",
            "value": f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "use": "work"
        }]
    }

def generate_encounter(patient_id: str, patient_name: str, org_id: str, practitioner_id: str, encounter_idx: int) -> Dict:
    """Generate an Encounter resource."""
    hash_val = hash_string(f"{patient_id}_encounter_{encounter_idx}")
    
    encounter_class = ENCOUNTER_CLASSES[int(hash_val[0:2], 16) % len(ENCOUNTER_CLASSES)]
    encounter_type = ENCOUNTER_TYPES[int(hash_val[2:4], 16) % len(ENCOUNTER_TYPES)]
    status = ENCOUNTER_STATUSES[int(hash_val[4:6], 16) % len(ENCOUNTER_STATUSES)]
    
    # Generate dates (1-18 months ago)
    months_ago = int(hash_val[6:8], 16) % 18 + 1
    start_date = datetime.now() - timedelta(days=months_ago * 30)
    start_date = start_date.replace(
        hour=random.randint(8, 17),
        minute=random.randint(0, 59)
    )
    duration_minutes = random.randint(15, 120)
    end_date = start_date + timedelta(minutes=duration_minutes)
    
    encounter_id = generate_resource_id("eEnc", f"{patient_id}_{encounter_idx}")
    participant_type = PARTICIPANT_TYPES[int(hash_val[8:10], 16) % len(PARTICIPANT_TYPES)]
    
    return {
        "resourceType": "Encounter",
        "id": encounter_id,
        "identifier": [{
            "use": "usual",
            "system": "urn:oid:1.2.840.114350.1.13.0.1.7.3.698084.8",
            "value": str(20000 + int(hash_val[10:14], 16) % 99999)
        }],
        "status": status,
        "class": {
            "system": "urn:oid:1.2.840.114350.1.72.1.7.7.10.696784.13260",
            "code": encounter_class["code"],
            "display": encounter_class["display"]
        },
        "type": [{
            "coding": [{
                "system": "urn:oid:1.2.840.114350.1.13.0.1.7.10.698084.10110",
                "code": encounter_type["code"],
                "display": encounter_type["display"]
            }],
            "text": encounter_type["text"]
        }],
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": patient_name
        },
        "participant": [{
            "type": [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                    "code": participant_type["code"],
                    "display": participant_type["display"]
                }],
                "text": participant_type["display"]
            }],
            "period": {
                "start": start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            },
            "individual": {
                "reference": f"Practitioner/{practitioner_id}",
                "type": "Practitioner",
                "display": "Physician, MD"
            }
        }],
        "period": {
            "start": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        },
        "account": [{
            "identifier": {
                "system": "urn:oid:1.2.840.114350.1.13.0.1.7.2.726582",
                "value": str(1000000 + int(hash_val[14:18], 16) % 999999)
            },
            "display": patient_name.replace(", ", ",").upper()
        }],
        "location": [{
            "location": {
                "reference": f"Location/{org_id}",
                "display": "Medical Center Location"
            }
        }],
        "serviceProvider": {
            "reference": f"Organization/{org_id}",
            "display": "Medical Center"
        }
    }

def generate_procedure(patient_id: str, patient_name: str, encounter_id: str, procedure_idx: int) -> Dict:
    """Generate a Procedure resource."""
    hash_val = hash_string(f"{patient_id}_procedure_{procedure_idx}")
    
    category = PROCEDURE_CATEGORIES[int(hash_val[0:2], 16) % len(PROCEDURE_CATEGORIES)]
    procedure_code = PROCEDURE_CODES[int(hash_val[2:4], 16) % len(PROCEDURE_CODES)]
    status = PROCEDURE_STATUSES[int(hash_val[4:6], 16) % len(PROCEDURE_STATUSES)]
    
    # Generate dates (1-5 years ago)
    years_ago = int(hash_val[6:8], 16) % 5 + 1
    performed_date = datetime.now() - timedelta(days=years_ago * 365)
    
    procedure_id = generate_resource_id("eProc", f"{patient_id}_{procedure_idx}")
    
    return {
        "resourceType": "Procedure",
        "id": procedure_id,
        "extension": [{
            "valueString": "Provider",
            "url": "http://open.epic.com/FHIR/StructureDefinition/extension/surgical-history-source"
        }],
        "status": status,
        "category": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": category["code"],
                "display": category["display"]
            }],
            "text": category["text"]
        },
        "code": {
            "text": procedure_code
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": patient_name
        },
        "performedDateTime": performed_date.strftime("%Y-%m-%d")
    }

def generate_observation(patient_id: str, patient_name: str, encounter_id: str, observation_idx: int) -> Dict:
    """Generate an Observation resource."""
    hash_val = hash_string(f"{patient_id}_observation_{observation_idx}")
    
    category = OBSERVATION_CATEGORIES[int(hash_val[0:2], 16) % len(OBSERVATION_CATEGORIES)]
    obs_code = OBSERVATION_CODES[int(hash_val[2:4], 16) % len(OBSERVATION_CODES)]
    status = OBSERVATION_STATUSES[int(hash_val[4:6], 16) % len(OBSERVATION_STATUSES)]
    
    # Generate dates (1-6 months ago)
    months_ago = int(hash_val[6:8], 16) % 6 + 1
    effective_date = datetime.now() - timedelta(days=months_ago * 30)
    effective_date = effective_date.replace(
        hour=random.randint(8, 17),
        minute=random.randint(0, 59)
    )
    
    observation_id = generate_resource_id("eObs", f"{patient_id}_{observation_idx}")
    
    # Generate value based on observation type
    if "Blood Pressure" in obs_code["display"]:
        value_text = f"{random.randint(100, 140)}/{random.randint(60, 90)} mmHg"
    elif "Heart Rate" in obs_code["display"]:
        value_text = f"{random.randint(60, 100)} bpm"
    elif "Temperature" in obs_code["display"]:
        value_text = f"{random.randint(97, 99)}.{(random.randint(0, 9))} F"
    elif "Glucose" in obs_code["display"]:
        value_text = f"{random.randint(70, 140)} mg/dL"
    else:
        value_text = "Normal"
    
    return {
        "resourceType": "Observation",
        "id": observation_id,
        "status": status,
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": category["code"],
                "display": category["display"]
            }],
            "text": category["text"]
        }],
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": obs_code["code"],
                "display": obs_code["display"]
            }],
            "text": obs_code["text"]
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": patient_name
        },
        "encounter": {
            "reference": encounter_id,
            "identifier": {
                "use": "usual",
                "system": "urn:oid:1.2.840.114350.1.13.11511.1.7.3.698084.8",
                "value": str(40000 + int(hash_val[8:12], 16) % 9999)
            },
            "display": "Encounter"
        },
        "effectiveDateTime": effective_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "issued": (effective_date + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "valueCodeableConcept": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": "17621005"
            }],
            "text": value_text
        },
        "interpretation": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                "code": "N",
                "display": "Normal"
            }],
            "text": "Normal"
        }]
    }

def generate_provenance(target_ref: str, practitioner_id: str, practitioner_name: str, org_id: str, prov_idx: int) -> Dict:
    """Generate a Provenance resource."""
    hash_val = hash_string(f"{target_ref}_provenance_{prov_idx}")
    
    agent_type = PROVENANCE_AGENT_TYPES[int(hash_val[0:2], 16) % len(PROVENANCE_AGENT_TYPES)]
    
    # Generate dates (1-12 months ago)
    months_ago = int(hash_val[2:4], 16) % 12 + 1
    recorded_date = datetime.now() - timedelta(days=months_ago * 30)
    recorded_date = recorded_date.replace(
        hour=random.randint(8, 17),
        minute=random.randint(0, 59)
    )
    
    provenance_id = generate_resource_id("eProv", f"{target_ref}_{prov_idx}")
    
    return {
        "resourceType": "Provenance",
        "id": provenance_id,
        "target": [{
            "reference": target_ref
        }],
        "recorded": recorded_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "agent": [{
            "type": {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/provenance-participant-type",
                    "code": agent_type["code"],
                    "display": agent_type["display"]
                }],
                "text": agent_type["text"]
            },
            "who": {
                "reference": f"Practitioner/{practitioner_id}",
                "display": practitioner_name
            },
            "onBehalfOf": {
                "display": "Medical Center"
            }
        }]
    }

def main():
    """Generate all remaining FHIR resources."""
    # Read existing data
    patients_path = Path("Sythetic_Data/patients.json")
    org_path = Path("Sythetic_Data/organisation.json")
    
    if not patients_path.exists() or not org_path.exists():
        print("Error: patients.json or organisation.json not found.")
        return
    
    with open(patients_path, "r", encoding="utf-8") as f:
        patients = json.load(f)
    
    with open(org_path, "r", encoding="utf-8") as f:
        organizations = json.load(f)
    
    output_dir = Path("Sythetic_Data")
    output_dir.mkdir(exist_ok=True)
    
    # Generate Practitioners (10 practitioners)
    practitioners = []
    for i in range(10):
        practitioners.append(generate_practitioner(i))
    
    practitioner_path = output_dir / "practitioner.json"
    with open(practitioner_path, "w", encoding="utf-8") as f:
        json.dump(practitioners, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(practitioners)} practitioners: {practitioner_path}")
    
    # Generate PractitionerRoles
    practitioner_roles = []
    for i, practitioner in enumerate(practitioners):
        practitioner_name = practitioner["name"][0]["text"]
        org_id = organizations[i % len(organizations)]["id"]
        # 1-2 roles per practitioner
        num_roles = (i % 2) + 1
        for role_idx in range(num_roles):
            practitioner_roles.append(generate_practitioner_role(
                practitioner["id"], practitioner_name, org_id, role_idx
            ))
    
    practitioner_role_path = output_dir / "practitonerrole.json"
    with open(practitioner_role_path, "w", encoding="utf-8") as f:
        json.dump(practitioner_roles, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(practitioner_roles)} practitioner roles: {practitioner_role_path}")
    
    # Generate Encounters (Bundle format)
    encounter_entries = []
    encounter_ids = []
    
    for patient in patients:
        patient_id = patient["id"]
        patient_name = get_patient_name(patient)
        org_id = organizations[patients.index(patient) % len(organizations)]["id"]
        practitioner_id = practitioners[patients.index(patient) % len(practitioners)]["id"]
        
        # 2-4 encounters per patient
        hash_val = hash_string(patient_id)
        num_encounters = (int(hash_val[0:2], 16) % 3) + 2
        
        for encounter_idx in range(num_encounters):
            encounter = generate_encounter(patient_id, patient_name, org_id, practitioner_id, encounter_idx)
            encounter_id = encounter["id"]
            encounter_ids.append((encounter_id, patient_id))
            
            entry = {
                "link": [{
                    "relation": "self",
                    "url": f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Encounter/{encounter_id}"
                }],
                "fullUrl": f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Encounter/{encounter_id}",
                "resource": encounter,
                "search": {"mode": "match"}
            }
            encounter_entries.append(entry)
    
    encounter_bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(encounter_entries),
        "link": [{
            "relation": "self",
            "url": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Encounter?patient=*&_count=100"
        }],
        "entry": encounter_entries
    }
    
    encounter_path = output_dir / "encounterr.json"
    with open(encounter_path, "w", encoding="utf-8") as f:
        json.dump(encounter_bundle, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(encounter_entries)} encounters: {encounter_path}")
    
    # Generate Procedures (Bundle format)
    procedure_entries = []
    
    for patient in patients:
        patient_id = patient["id"]
        patient_name = get_patient_name(patient)
        
        # Use first encounter for this patient
        patient_encounters = [enc_id for enc_id, pat_id in encounter_ids if pat_id == patient_id]
        encounter_ref = f"Encounter/{patient_encounters[0]}" if patient_encounters else None
        
        # 1-3 procedures per patient
        hash_val = hash_string(patient_id)
        num_procedures = (int(hash_val[2:4], 16) % 3) + 1
        
        for procedure_idx in range(num_procedures):
            procedure = generate_procedure(patient_id, patient_name, encounter_ref or "", procedure_idx)
            
            entry = {
                "link": [{
                    "relation": "self",
                    "url": f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Procedure/{procedure['id']}"
                }],
                "fullUrl": f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Procedure/{procedure['id']}",
                "resource": procedure,
                "search": {"mode": "match"}
            }
            procedure_entries.append(entry)
    
    procedure_bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(procedure_entries),
        "link": [{
            "relation": "self",
            "url": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Procedure?patient=*&_count=100"
        }],
        "entry": procedure_entries
    }
    
    procedure_path = output_dir / "procedure.json"
    with open(procedure_path, "w", encoding="utf-8") as f:
        json.dump(procedure_bundle, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(procedure_entries)} procedures: {procedure_path}")
    
    # Generate Observations
    observations = []
    
    for patient in patients:
        patient_id = patient["id"]
        patient_name = get_patient_name(patient)
        
        # Use encounters for this patient
        patient_encounters = [enc_id for enc_id, pat_id in encounter_ids if pat_id == patient_id]
        
        # 3-6 observations per patient
        hash_val = hash_string(patient_id)
        num_observations = (int(hash_val[4:6], 16) % 4) + 3
        
        for obs_idx in range(num_observations):
            encounter_ref = f"Encounter/{patient_encounters[obs_idx % len(patient_encounters)]}" if patient_encounters else None
            if not encounter_ref:
                continue
            observation = generate_observation(patient_id, patient_name, encounter_ref, obs_idx)
            observations.append(observation)
    
    observation_path = output_dir / "observation.json"
    with open(observation_path, "w", encoding="utf-8") as f:
        json.dump(observations, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(observations)} observations: {observation_path}")
    
    # Generate EOB (ExplanationOfBenefit) - Bundle with OperationOutcome (empty results)
    eob_bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": 0,
        "link": [{
            "relation": "self",
            "url": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/ExplanationOfBenefit?patient=*&_count=100"
        }],
        "entry": [{
            "fullUrl": "urn:uuid:d864bb09-2e8b-47ac-9cb0-6e3a46dc6613",
            "resource": {
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "warning",
                        "code": "suppressed",
                        "details": {
                            "coding": [{
                                "system": "urn:oid:1.2.840.114350.1.13.0.1.7.2.657369",
                                "code": "59204",
                                "display": "The authenticated client's search request applies to a sub-resource that the client is not authorized for."
                            }],
                            "text": "The authenticated client's search request applies to a sub-resource that the client is not authorized for."
                        },
                        "diagnostics": "Client not authorized for ExplanationOfBenefit - Prior Auth."
                    },
                    {
                        "severity": "warning",
                        "code": "processing",
                        "details": {
                            "coding": [{
                                "system": "urn:oid:1.2.840.114350.1.13.0.1.7.2.657369",
                                "code": "4101",
                                "display": "Resource request returns no results."
                            }],
                            "text": "Resource request returns no results."
                        }
                    }
                ]
            },
            "search": {
                "mode": "outcome"
            }
        }]
    }
    
    eob_path = output_dir / "eob.json"
    with open(eob_path, "w", encoding="utf-8") as f:
        json.dump(eob_bundle, f, indent=2, ensure_ascii=False)
    print(f"Generated EOB bundle: {eob_path}")
    
    # Generate Provenance resources
    provenances = []
    
    # Create provenance for various resources
    for i, patient in enumerate(patients):
        patient_id = patient["id"]
        practitioner_id = practitioners[i % len(practitioners)]["id"]
        practitioner_name = practitioners[i % len(practitioners)]["name"][0]["text"]
        org_id = organizations[i % len(organizations)]["id"]
        
        # Generate provenance for Patient, Condition, Procedure, Observation
        provenances.append(generate_provenance(f"Patient/{patient_id}", practitioner_id, practitioner_name, org_id, 0))
        provenances.append(generate_provenance(f"Condition/eCond{hash_string(patient_id)[:20]}", practitioner_id, practitioner_name, org_id, 1))
        provenances.append(generate_provenance(f"Procedure/eProc{hash_string(patient_id)[:20]}", practitioner_id, practitioner_name, org_id, 2))
    
    provenance_path = output_dir / "provenance.json"
    with open(provenance_path, "w", encoding="utf-8") as f:
        json.dump(provenances, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(provenances)} provenance resources: {provenance_path}")

if __name__ == "__main__":
    main()

