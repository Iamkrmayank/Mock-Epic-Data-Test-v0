import json
import hashlib
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# Patient and Organization IDs provided by user
PATIENT_ORG_PAIRS = [
    ("ePtdJFCrnl2edlBDdz1C5Ja", "eLJ.EJ4jKEIQOkrtDXtBi10Q71hA1XcW9a"),
    ("ePt2RJtBRnlWmTSHf6pWkLUy", "eLGk8cgSCifdFzctEq8oB7GVvouNndNWYzjFn"),
    ("ePtfDLkDmWJ6UuVTAIjvFu7", "eLMX1C.CI3.dXRZv7qdYdk2r7xgHWPB6PRWJ"),
    ("ePtICPhDeOZIiBOB-Y6sHrFH2ZUC", "eLpfS2ViRb1.n3U6t3wI973IPFlJ5F7WRd-"),
    ("ePt-lgotu2iXW7GboIRoL3u6", "eLDpyOpxyB9JKmyLDUwMbqJfgLq.nbK894R"),
    ("ePtHwnMztVuaP.coUNEhEk", "eLI-4kf3PGdlDcIfw84Jx3.l8S0QPnuQ0-KZe"),
    ("ePt.iqq8vH2BzNZV45pFCiR", "eLx.BTHRJJbykE0.E8.5clLCZFNV8S2QT6IN"),
    ("ePtDCajhDieQjEJ.Bq8F80", "eLgG9oiZ.jgttMkFp1CW54M2NhmABHkuE"),
    ("ePtmm3T207gmhZRnFyy5r2xJ7", "eLjua058LeDKK6jDHz2oCtIsjhvNK4p7M"),
    ("ePtj4mgblEv0.9BZhvWaXH6K2", "eLlOGPoZa70gyU-4gAIqK4.pdEuNb0lCo7pt-L"),
]

# Synthetic data generators
FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Christopher", "Karen", "Daniel", "Nancy", "Matthew", "Lisa",
    "Anthony", "Betty", "Mark", "Margaret", "Donald", "Sandra", "Steven", "Ashley",
    "Paul", "Kimberly", "Andrew", "Emily", "Joshua", "Donna", "Kenneth", "Michelle"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor",
    "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris", "Clark",
    "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott"
]

US_CITIES = [
    ("Chicago", "IL", "60601"), ("New York", "NY", "10001"), ("Los Angeles", "CA", "90001"),
    ("Houston", "TX", "77001"), ("Phoenix", "AZ", "85001"), ("Philadelphia", "PA", "19101"),
    ("San Antonio", "TX", "78201"), ("San Diego", "CA", "92101"), ("Dallas", "TX", "75201"),
    ("San Jose", "CA", "95101"), ("Austin", "TX", "78701"), ("Jacksonville", "FL", "32099"),
    ("Fort Worth", "TX", "76101"), ("Columbus", "OH", "43201"), ("Charlotte", "NC", "28201"),
    ("San Francisco", "CA", "94101"), ("Indianapolis", "IN", "46201"), ("Seattle", "WA", "98101"),
    ("Denver", "CO", "80201"), ("Boston", "MA", "02101")
]

INSURANCE_TYPES = ["PPO", "HMO", "EPO", "Medicare Advantage"]
INSURANCE_NAMES = ["Aetna", "Blue Cross Blue Shield", "UnitedHealthcare", "Cigna", "Humana", "Kaiser Permanente"]

HOSPITAL_NAMES = [
    "Regional Medical Center", "Community Hospital", "General Health System", 
    "Metropolitan Medical Center", "Valley Hospital", "Memorial Hospital",
    "City Medical Center", "Riverside Hospital", "University Medical Center",
    "Central Hospital"
]

def hash_string(s: str) -> str:
    """Generate hash from string for deterministic but varied values."""
    return hashlib.md5(s.encode()).hexdigest()

def last_n_digits(s: str, n: int) -> str:
    """Get last n characters from hash."""
    h = hash_string(s)
    return h[-n:]

def generate_mrn(patient_id: str) -> str:
    """Generate MRN from patient ID."""
    return f"MRN-{last_n_digits(patient_id, 6)}"

def generate_member_id(patient_id: str) -> str:
    """Generate insurance member ID from patient ID."""
    return f"MBR-{last_n_digits(patient_id, 7)}"

def generate_ssn() -> str:
    """Generate synthetic SSN starting with 9."""
    return f"9{random.randint(10, 99)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"

def generate_phone() -> str:
    """Generate US phone number."""
    area = random.randint(200, 999)
    exchange = random.randint(200, 999)
    number = random.randint(1000, 9999)
    return f"+1-{area}-{exchange}-{number:04d}"

def generate_birth_date(age_min: int = 18, age_max: int = 85) -> str:
    """Generate birth date for age between min and max."""
    age = random.randint(age_min, age_max)
    birth_year = datetime.now().year - age
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{birth_year}-{month:02d}-{day:02d}"

def generate_patient(patient_id: str, org_id: str, org_name: str = "Medical Center") -> Dict:
    """Generate a Patient resource matching Epic structure."""
    # Deterministic selection based on patient_id
    hash_val = hash_string(patient_id)
    gender_idx = int(hash_val[0], 16) % 2
    gender = "female" if gender_idx == 0 else "male"
    
    first_name = FIRST_NAMES[int(hash_val[1:3], 16) % len(FIRST_NAMES)]
    last_name = LAST_NAMES[int(hash_val[3:5], 16) % len(LAST_NAMES)]
    
    city_idx = int(hash_val[5:7], 16) % len(US_CITIES)
    city, state, zip_code = US_CITIES[city_idx]
    
    street_num = random.randint(100, 9999)
    street_name = ["Main", "Oak", "Park", "First", "Second", "Maple", "Cedar", "Elm"][int(hash_val[7:9], 16) % 8]
    street = f"{street_num} {street_name} Street"
    
    birth_date = generate_birth_date()
    
    # Generate extensions for gender/sex
    legal_sex_code = "female" if gender == "female" else "male"
    clinical_sex_code = "248152002" if gender == "female" else "248153007"
    
    return {
        "resourceType": "Patient",
        "id": patient_id,
        "data": {
            "resourceType": "Patient",
            "id": patient_id,
            "extension": [
                {
                    "valueCodeableConcept": {
                        "coding": [{
                            "system": "urn:oid:1.2.840.114350.1.13.0.1.7.10.698084.130.657370.19999000",
                            "code": legal_sex_code,
                            "display": legal_sex_code
                        }],
                        "text": legal_sex_code.capitalize()
                    },
                    "url": "http://open.epic.com/FHIR/StructureDefinition/extension/legal-sex"
                },
                {
                    "valueCodeableConcept": {
                        "coding": [{
                            "system": "urn:oid:1.2.840.114350.1.13.0.1.7.10.698084.130.657370.19999000",
                            "code": legal_sex_code,
                            "display": legal_sex_code
                        }]
                    },
                    "url": "http://open.epic.com/FHIR/StructureDefinition/extension/sex-for-clinical-use"
                },
                {
                    "extension": [
                        {
                            "valueCoding": {
                                "system": "urn:oid:2.16.840.1.113883.6.238",
                                "code": "2106-3",
                                "display": "White"
                            },
                            "url": "ombCategory"
                        },
                        {
                            "valueString": "White",
                            "url": "text"
                        }
                    ],
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race"
                },
                {
                    "extension": [
                        {
                            "valueString": "Not Hispanic or Latino",
                            "url": "text"
                        }
                    ],
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity"
                },
                {
                    "valueCode": clinical_sex_code,
                    "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-sex"
                },
                {
                    "valueCodeableConcept": {
                        "coding": [{
                            "system": "http://loinc.org",
                            "code": "LA29519-8" if gender == "female" else "LA29520-6",
                            "display": "she/her/her/hers/herself" if gender == "female" else "he/him/his/his/himself"
                        }]
                    },
                    "url": "http://open.epic.com/FHIR/StructureDefinition/extension/calculated-pronouns-to-use-for-text"
                }
            ],
            "identifier": [
                {
                    "use": "usual",
                    "type": {"text": "MRN"},
                    "system": "urn:mrn:gooclaim",
                    "value": generate_mrn(patient_id)
                },
                {
                    "use": "usual",
                    "type": {"text": "FHIR STU3"},
                    "system": "http://open.epic.com/FHIR/StructureDefinition/patient-fhir-id",
                    "value": patient_id
                },
                {
                    "use": "usual",
                    "type": {"text": "Insurance Member ID"},
                    "system": "urn:memberid:gooclaim",
                    "value": generate_member_id(patient_id)
                }
            ],
            "active": True,
            "name": [{
                "use": "official",
                "text": f"{first_name} {last_name}",
                "family": last_name,
                "given": [first_name]
            }, {
                "use": "usual",
                "text": f"{first_name} {last_name}",
                "family": last_name,
                "given": [first_name]
            }],
            "gender": gender,
            "birthDate": birth_date,
            "deceasedBoolean": False,
            "address": [{
                "use": "home",
                "text": f"{street}\\r\\n{city} {state} {zip_code}\\r\\nUnited States of America",
                "line": [street],
                "city": city,
                "state": state,
                "postalCode": zip_code,
                "country": "US",
                "period": {
                    "start": "2010-01-01"
                }
            }],
            "telecom": [{
                "system": "phone",
                "value": generate_phone(),
                "use": "home"
            }],
            "maritalStatus": {
                "text": random.choice(["Married", "Single", "Divorced", "Widowed"])
            },
            "managingOrganization": {
                "reference": f"Organization/{org_id}",
                "display": org_name
            }
        },
        "retrieved_at": datetime.now().isoformat() + "+00:00"
    }

def generate_organization(org_id: str, index: int) -> Dict:
    """Generate an Organization resource."""
    hash_val = hash_string(org_id)
    hospital_name = HOSPITAL_NAMES[index % len(HOSPITAL_NAMES)]
    city_idx = int(hash_val[0:2], 16) % len(US_CITIES)
    city, state, zip_code = US_CITIES[city_idx]
    
    street_num = random.randint(100, 9999)
    street_name = ["Medical", "Hospital", "Health", "Care", "Center"][int(hash_val[2:4], 16) % 5]
    street = f"{street_num} {street_name} Boulevard"
    
    npi = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    tax_id = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    
    return {
        "resourceType": "Organization",
        "id": org_id,
        "identifier": [
            {
                "use": "usual",
                "type": {"text": "NPI"},
                "system": "http://hl7.org/fhir/sid/us-npi",
                "value": npi
            },
            {
                "use": "usual",
                "type": {"text": "TAX"},
                "system": "urn:oid:2.16.840.1.113883.4.4",
                "value": tax_id
            },
            {
                "use": "usual",
                "system": "urn:oid:1.2.840.114350.1.13.0.1.7.2.696570",
                "value": last_n_digits(org_id, 5)
            }
        ],
        "active": True,
        "name": hospital_name,
        "address": [{
            "text": f"{street}\\r\\n{city} {state} {zip_code}\\r\\nUnited States of America",
            "line": [street],
            "city": city,
            "state": state,
            "postalCode": zip_code,
            "country": "United States of America"
        }]
    }

def generate_coverage(patient_id: str, org_id: str, org_name: str) -> Dict:
    """Generate a Coverage resource."""
    hash_val = hash_string(patient_id)
    insurance_type = INSURANCE_TYPES[int(hash_val[0], 16) % len(INSURANCE_TYPES)]
    insurance_name = INSURANCE_NAMES[int(hash_val[1], 16) % len(INSURANCE_NAMES)]
    
    # Coverage period: current month +/- a few months
    start_date = datetime.now() - timedelta(days=random.randint(30, 365))
    end_date = start_date + timedelta(days=random.randint(365, 730))
    
    plan_code = last_n_digits(patient_id, 5)
    
    return {
        "id": f"cov-{patient_id}",
        "status": "active",
        "type": None,
        "subscriber": "",
        "subscriber_id": None,
        "beneficiary": f"Patient/{patient_id}",
        "relationship": None,
        "period": None,
        "payor": [{
            "reference": f"Organization/{org_id}",
            "display": org_name
        }],
        "class": [{
            "type": {
                "code": "plan",
                "display": "Plan"
            },
            "value": plan_code,
            "name": insurance_name
        }, {
            "type": {
                "code": "group",
                "display": "Group"
            },
            "value": f"GRP-{plan_code}",
            "name": insurance_name
        }],
        "network": None,
        "cost_sharing": []
    }

def main():
    """Generate all synthetic FHIR data files."""
    output_dir = Path("Sythetic_Data")
    output_dir.mkdir(exist_ok=True)
    
    patients = []
    organizations = []
    coverages = []
    org_map = {}  # Map org_id to org_name
    
    for idx, (patient_id, org_id) in enumerate(PATIENT_ORG_PAIRS):
        # Generate organization first (only once per unique org_id)
        if org_id not in org_map:
            org = generate_organization(org_id, idx)
            organizations.append(org)
            org_map[org_id] = org["name"]
        
        # Generate patient with org name
        patient = generate_patient(patient_id, org_id, org_map[org_id])
        patients.append(patient)
        
        # Generate coverage
        coverage = generate_coverage(patient_id, org_id, org_map[org_id])
        coverages.append(coverage)
    
    # Save patients.json (array format)
    patients_path = output_dir / "patients.json"
    with open(patients_path, "w", encoding="utf-8") as f:
        json.dump(patients, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(patients)} patients: {patients_path}")
    
    # Save organisation.json (array format)
    org_path = output_dir / "organisation.json"
    with open(org_path, "w", encoding="utf-8") as f:
        json.dump(organizations, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(organizations)} organizations: {org_path}")
    
    # Save coverage.json (with total and coverage array)
    coverage_path = output_dir / "coverage.json"
    coverage_data = {
        "total": len(coverages),
        "coverage": coverages
    }
    with open(coverage_path, "w", encoding="utf-8") as f:
        json.dump(coverage_data, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(coverages)} coverages: {coverage_path}")

if __name__ == "__main__":
    main()

