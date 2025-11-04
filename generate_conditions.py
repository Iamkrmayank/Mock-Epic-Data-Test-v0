import json
import hashlib
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# Common medical conditions with ICD-10, SNOMED, ICD-9 codes
MEDICAL_CONDITIONS = [
    {
        "icd10": {"code": "I10", "display": "Essential (primary) hypertension"},
        "snomed": {"code": "38341003", "display": "Hypertensive Disorder"},
        "icd9": {"code": "401.9", "display": "Hypertension"},
        "text": "Hypertension"
    },
    {
        "icd10": {"code": "E11.9", "display": "Type 2 diabetes mellitus without complications"},
        "snomed": {"code": "44054006", "display": "Diabetes mellitus type 2"},
        "icd9": {"code": "250.00", "display": "Diabetes mellitus without mention of complication"},
        "text": "Type 2 Diabetes"
    },
    {
        "icd10": {"code": "M81.0", "display": "Age-related osteoporosis without current pathological fracture"},
        "snomed": {"code": "64859006", "display": "Osteoporosis"},
        "icd9": {"code": "733.00", "display": "Osteoporosis"},
        "text": "Osteoporosis"
    },
    {
        "icd10": {"code": "J44.1", "display": "Chronic obstructive pulmonary disease with acute exacerbation"},
        "snomed": {"code": "13645005", "display": "Chronic obstructive lung disease"},
        "icd9": {"code": "496", "display": "Chronic airway obstruction"},
        "text": "COPD"
    },
    {
        "icd10": {"code": "M79.3", "display": "Panniculitis, unspecified"},
        "snomed": {"code": "23878001", "display": "Fibromyalgia"},
        "icd9": {"code": "729.1", "display": "Myalgia and myositis"},
        "text": "Fibromyalgia"
    },
    {
        "icd10": {"code": "K21.9", "display": "Gastro-esophageal reflux disease without esophagitis"},
        "snomed": {"code": "235595009", "display": "Gastroesophageal reflux disease"},
        "icd9": {"code": "530.81", "display": "Esophageal reflux"},
        "text": "GERD"
    },
    {
        "icd10": {"code": "E78.5", "display": "Hyperlipidemia, unspecified"},
        "snomed": {"code": "55822004", "display": "Hyperlipidemia"},
        "icd9": {"code": "272.4", "display": "Other and unspecified hyperlipidemia"},
        "text": "Hyperlipidemia"
    },
    {
        "icd10": {"code": "G47.33", "display": "Obstructive sleep apnea"},
        "snomed": {"code": "73443001", "display": "Sleep apnea"},
        "icd9": {"code": "780.57", "display": "Sleep apnea"},
        "text": "Sleep Apnea"
    },
    {
        "icd10": {"code": "M25.511", "display": "Pain in right shoulder"},
        "snomed": {"code": "298705000", "display": "Pain in shoulder"},
        "icd9": {"code": "719.41", "display": "Pain in joint, shoulder region"},
        "text": "Shoulder Pain"
    },
    {
        "icd10": {"code": "M54.5", "display": "Low back pain"},
        "snomed": {"code": "161891005", "display": "Low back pain"},
        "icd9": {"code": "724.2", "display": "Low back pain"},
        "text": "Low Back Pain"
    },
    {
        "icd10": {"code": "F41.9", "display": "Anxiety disorder, unspecified"},
        "snomed": {"code": "48694002", "display": "Anxiety disorder"},
        "icd9": {"code": "300.00", "display": "Anxiety state"},
        "text": "Anxiety"
    },
    {
        "icd10": {"code": "F32.9", "display": "Major depressive disorder, single episode, unspecified"},
        "snomed": {"code": "35489007", "display": "Depressive disorder"},
        "icd9": {"code": "296.20", "display": "Major depressive affective disorder"},
        "text": "Depression"
    },
    {
        "icd10": {"code": "K59.00", "display": "Constipation, unspecified"},
        "snomed": {"code": "14760008", "display": "Constipation"},
        "icd9": {"code": "564.00", "display": "Constipation"},
        "text": "Constipation"
    },
    {
        "icd10": {"code": "N18.6", "display": "End stage renal disease"},
        "snomed": {"code": "42399005", "display": "Chronic kidney disease"},
        "icd9": {"code": "585.9", "display": "Chronic kidney disease"},
        "text": "Chronic Kidney Disease"
    },
    {
        "icd10": {"code": "I25.10", "display": "Atherosclerotic heart disease of native coronary artery without angina pectoris"},
        "snomed": {"code": "53741008", "display": "Coronary artery disease"},
        "icd9": {"code": "414.00", "display": "Coronary atherosclerosis"},
        "text": "Coronary Artery Disease"
    }
]

CLINICAL_STATUSES = [
    {"code": "active", "display": "Active", "text": "Active"},
    {"code": "recurrence", "display": "Recurrence", "text": "Recurrence"},
    {"code": "remission", "display": "Remission", "text": "Remission"},
    {"code": "inactive", "display": "Inactive", "text": "Inactive"}
]

VERIFICATION_STATUSES = [
    {"code": "confirmed", "display": "Confirmed", "text": "Confirmed"},
    {"code": "unconfirmed", "display": "Unconfirmed", "text": "Unconfirmed"},
    {"code": "refuted", "display": "Refuted", "text": "Refuted"}
]

CATEGORIES = [
    {"code": "problem-list-item", "display": "Problem List Item", "text": "Problem List Item"},
    {"code": "encounter-diagnosis", "display": "Encounter Diagnosis", "text": "Encounter Diagnosis"}
]

def hash_string(s: str) -> str:
    """Generate hash from string for deterministic selection."""
    return hashlib.md5(s.encode()).hexdigest()

def generate_condition_id(patient_id: str, condition_idx: int) -> str:
    """Generate a deterministic condition ID."""
    hash_val = hash_string(f"{patient_id}_{condition_idx}")
    return f"eCond{hash_val[:20]}"

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

def generate_condition(patient_id: str, patient_name: str, condition_idx: int) -> Dict:
    """Generate a Condition resource."""
    # Deterministic selection based on patient_id and condition_idx
    hash_val = hash_string(f"{patient_id}_{condition_idx}")
    
    # Select condition
    condition = MEDICAL_CONDITIONS[int(hash_val[0:2], 16) % len(MEDICAL_CONDITIONS)]
    
    # Select statuses
    clinical_status = CLINICAL_STATUSES[int(hash_val[2:4], 16) % len(CLINICAL_STATUSES)]
    verification_status = VERIFICATION_STATUSES[int(hash_val[4:6], 16) % len(VERIFICATION_STATUSES)]
    
    # Select category
    category = CATEGORIES[int(hash_val[6:8], 16) % len(CATEGORIES)]
    
    # Generate dates (onset 1-10 years ago, recorded same or later)
    years_ago = int(hash_val[8:10], 16) % 10 + 1
    onset_date = (datetime.now() - timedelta(days=years_ago * 365)).strftime("%Y-%m-%d")
    days_after_onset = int(hash_val[10:12], 16) % 30
    recorded_date = (datetime.strptime(onset_date, "%Y-%m-%d") + timedelta(days=days_after_onset)).strftime("%Y-%m-%d")
    
    condition_id = generate_condition_id(patient_id, condition_idx)
    
    # Build condition resource
    condition_resource = {
        "resourceType": "Condition",
        "id": condition_id,
        "clinicalStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "version": "4.0.0",
                "code": clinical_status["code"],
                "display": clinical_status["display"]
            }],
            "text": clinical_status["text"]
        },
        "verificationStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "version": "4.0.0",
                "code": verification_status["code"],
                "display": verification_status["display"]
            }],
            "text": verification_status["text"]
        },
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                "code": category["code"],
                "display": category["display"]
            }],
            "text": category["text"]
        }],
        "code": {
            "coding": [
                {
                    "system": "http://hl7.org/fhir/sid/icd-10-cm",
                    "code": condition["icd10"]["code"],
                    "display": condition["icd10"]["display"]
                },
                {
                    "system": "http://snomed.info/sct",
                    "code": condition["snomed"]["code"],
                    "display": condition["snomed"]["display"]
                },
                {
                    "system": "http://hl7.org/fhir/sid/icd-9-cm",
                    "code": condition["icd9"]["code"],
                    "display": condition["icd9"]["display"]
                }
            ],
            "text": condition["text"]
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": patient_name
        },
        "onsetDateTime": onset_date,
        "recordedDate": recorded_date
    }
    
    # Add note for some conditions (30% chance)
    if int(hash_val[12:14], 16) % 100 < 30:
        note_time = datetime.strptime(recorded_date, "%Y-%m-%d")
        note_time = note_time.replace(hour=random.randint(8, 17), minute=random.randint(0, 59))
        
        condition_resource["note"] = [{
            "extension": [
                {
                    "valueString": "Formatting of this note might be different from the original.",
                    "url": "http://open.epic.com/FHIR/StructureDefinition/extension/data-conversion-warning"
                },
                {
                    "valueCodeableConcept": {
                        "coding": [{
                            "system": "http://loinc.org",
                            "code": "68608-9",
                            "display": "Summary note"
                        }],
                        "text": "Problem Overview"
                    },
                    "url": "http://hl7.org/fhir/StructureDefinition/annotationType"
                }
            ],
            "authorReference": {
                "reference": "Practitioner/ePractitioner123",
                "display": "Physician, MD"
            },
            "time": note_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "text": f"Condition noted during routine visit. Patient reports stable condition."
        }]
    
    return condition_resource

def generate_conditions_bundle(patients: List[Dict]) -> Dict:
    """Generate a Bundle of Condition resources for all patients."""
    entries = []
    total_conditions = 0
    
    for patient in patients:
        patient_id = patient["id"]
        patient_data = patient.get("data", patient)
        patient_name = get_patient_name(patient)
        
        # Generate 2-5 conditions per patient
        hash_val = hash_string(patient_id)
        num_conditions = (int(hash_val[0:2], 16) % 4) + 2  # 2-5 conditions
        
        for condition_idx in range(num_conditions):
            condition_resource = generate_condition(patient_id, patient_name, condition_idx)
            condition_id = condition_resource["id"]
            
            entry = {
                "link": [{
                    "relation": "self",
                    "url": f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Condition/{condition_id}"
                }],
                "fullUrl": f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Condition/{condition_id}",
                "resource": condition_resource,
                "search": {
                    "mode": "match"
                }
            }
            entries.append(entry)
            total_conditions += 1
    
    bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": total_conditions,
        "link": [{
            "relation": "self",
            "url": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Condition?patient=*&_count=100"
        }],
        "entry": entries
    }
    
    return bundle

def main():
    """Generate conditions.json file."""
    # Read patients
    patients_path = Path("Sythetic_Data/patients.json")
    if not patients_path.exists():
        print(f"Error: {patients_path} not found. Please generate patients first.")
        return
    
    with open(patients_path, "r", encoding="utf-8") as f:
        patients = json.load(f)
    
    # Generate conditions bundle
    bundle = generate_conditions_bundle(patients)
    
    # Save conditions
    output_dir = Path("Sythetic_Data")
    output_dir.mkdir(exist_ok=True)
    
    conditions_path = output_dir / "conditionss.json"
    with open(conditions_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {bundle['total']} conditions for {len(patients)} patients: {conditions_path}")

if __name__ == "__main__":
    main()

