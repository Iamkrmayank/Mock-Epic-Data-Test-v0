import json
import hashlib
import base64
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# Consent types
CONSENT_SCOPES = [
    {"code": "2000", "display": "Consent Form", "text": "Consent Form"},
    {"code": "11", "display": "Power of Attorney", "text": "Power of Attorney"},
    {"code": "12", "display": "HIPAA Notice of Privacy", "text": "HIPAA Notice of Privacy"},
    {"code": "13", "display": "Advanced Directive", "text": "Advanced Directive"},
    {"code": "14", "display": "Research Consent", "text": "Research Consent"}
]

CONSENT_STATUSES = ["draft", "proposed", "active", "rejected", "inactive"]

# Document types
DOCUMENT_TYPES = [
    {
        "code": "1",
        "display": "Progress Notes",
        "text": "Progress Notes",
        "loinc": {"code": "11506-3", "display": "Progress note"}
    },
    {
        "code": "2",
        "display": "Discharge Summary",
        "text": "Discharge Summary",
        "loinc": {"code": "18842-5", "display": "Discharge summary"}
    },
    {
        "code": "3",
        "display": "Lab Results",
        "text": "Lab Results",
        "loinc": {"code": "26436-6", "display": "Laboratory studies"}
    },
    {
        "code": "4",
        "display": "Imaging Report",
        "text": "Imaging Report",
        "loinc": {"code": "18726-0", "display": "Radiology studies"}
    },
    {
        "code": "5",
        "display": "Consultation Note",
        "text": "Consultation Note",
        "loinc": {"code": "11488-4", "display": "Consult note"}
    }
]

DOCUMENT_CATEGORIES = [
    {"code": "clinical-note", "display": "Clinical Note", "text": "Clinical Note"},
    {"code": "lab-report", "display": "Lab Report", "text": "Lab Report"},
    {"code": "imaging-report", "display": "Imaging Report", "text": "Imaging Report"}
]

DOCUMENT_STATUSES = ["current", "superseded", "entered-in-error"]
DOC_STATUSES = ["preliminary", "final", "amended", "entered-in-error", "unknown"]

# Binary content types
BINARY_CONTENT_TYPES = [
    "text/rtf",
    "text/html",
    "application/pdf",
    "application/xml",
    "text/plain"
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

def generate_consent(patient_id: str, patient_name: str, consent_idx: int) -> Dict:
    """Generate a Consent resource."""
    hash_val = hash_string(f"{patient_id}_consent_{consent_idx}")
    
    # Select scope/category
    scope = CONSENT_SCOPES[int(hash_val[0:2], 16) % len(CONSENT_SCOPES)]
    status = CONSENT_STATUSES[int(hash_val[2:4], 16) % len(CONSENT_STATUSES)]
    
    # Generate dates (1-5 years ago)
    years_ago = int(hash_val[4:6], 16) % 5 + 1
    consent_date = (datetime.now() - timedelta(days=years_ago * 365))
    consent_date = consent_date.replace(
        hour=random.randint(8, 17),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )
    
    consent_id = generate_resource_id("eConsent", f"{patient_id}_{consent_idx}")
    
    consent_resource = {
        "resourceType": "Consent",
        "id": consent_id,
        "identifier": [{
            "use": "usual",
            "system": "urn:oid:1.2.840.114350.1.13.0.1.7.2.686783",
            "value": str(700000 + int(hash_val[6:10], 16) % 99999)
        }],
        "status": status,
        "scope": {
            "coding": [{
                "system": "urn:oid:1.2.840.114350.1.13.0.1.7.4.686783.100",
                "code": scope["code"],
                "display": scope["display"]
            }],
            "text": scope["text"]
        },
        "category": [{
            "coding": [
                {
                    "system": "urn:oid:1.2.840.114350.1.13.0.1.7.4.686783.100",
                    "code": scope["code"],
                    "display": scope["display"]
                },
                {
                    "system": "http://loinc.org",
                    "code": "59284-0",
                    "display": "Consent Document"
                }
            ],
            "text": "Consent Document"
        }],
        "patient": {
            "reference": f"Patient/{patient_id}",
            "display": patient_name
        },
        "dateTime": consent_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "policy": [{
            "extension": [{
                "valueCode": "unknown",
                "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason"
            }]
        }]
    }
    
    # Add provision for some consents (40% chance)
    if int(hash_val[10:12], 16) % 100 < 40:
        consent_resource["provision"] = {
            "data": [{
                "meaning": "related",
                "reference": {
                    "reference": f"Encounter/eEnc{hash_val[12:20]}"
                }
            }]
        }
    
    # Add _status extension for some (30% chance)
    if int(hash_val[12:14], 16) % 100 < 30:
        consent_resource["_status"] = {
            "extension": [{
                "valueCode": "unknown",
                "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason"
            }]
        }
    
    return consent_resource

def generate_binary(patient_id: str, binary_idx: int) -> Dict:
    """Generate a Binary resource."""
    hash_val = hash_string(f"{patient_id}_binary_{binary_idx}")
    
    binary_id = generate_resource_id("eBinary", f"{patient_id}_{binary_idx}")
    content_type = BINARY_CONTENT_TYPES[int(hash_val[0:2], 16) % len(BINARY_CONTENT_TYPES)]
    
    # Generate synthetic base64-encoded content (simulating RTF/HTML/PDF)
    if content_type == "text/rtf":
        # Simulate RTF content
        fake_rtf = "{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Times New Roman;}} This is a synthetic RTF document.\\par}"
        data = base64.b64encode(fake_rtf.encode('utf-8')).decode('ascii')
    elif content_type == "text/html":
        fake_html = "<html><body><h1>Clinical Document</h1><p>This is a synthetic HTML document.</p></body></html>"
        data = base64.b64encode(fake_html.encode('utf-8')).decode('ascii')
    elif content_type == "application/pdf":
        # Minimal PDF header (not a real PDF, just for demo)
        fake_pdf = "%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\nxref\n0 1\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
        data = base64.b64encode(fake_pdf.encode('utf-8')).decode('ascii')
    else:
        fake_text = f"This is a synthetic document for patient {patient_id[:10]}..."
        data = base64.b64encode(fake_text.encode('utf-8')).decode('ascii')
    
    return {
        "resourceType": "Binary",
        "id": binary_id,
        "contentType": content_type,
        "data": data
    }

def generate_document_reference(patient_id: str, patient_name: str, doc_idx: int) -> Dict:
    """Generate a DocumentReference resource."""
    hash_val = hash_string(f"{patient_id}_docref_{doc_idx}")
    
    doc_id = generate_resource_id("eDocRef", f"{patient_id}_{doc_idx}")
    doc_type = DOCUMENT_TYPES[int(hash_val[0:2], 16) % len(DOCUMENT_TYPES)]
    category = DOCUMENT_CATEGORIES[int(hash_val[2:4], 16) % len(DOCUMENT_CATEGORIES)]
    status = DOCUMENT_STATUSES[int(hash_val[4:6], 16) % len(DOCUMENT_STATUSES)]
    doc_status = DOC_STATUSES[int(hash_val[6:8], 16) % len(DOC_STATUSES)]
    
    # Generate dates (1-12 months ago)
    months_ago = int(hash_val[8:10], 16) % 12 + 1
    doc_date = datetime.now() - timedelta(days=months_ago * 30)
    doc_date = doc_date.replace(
        hour=random.randint(8, 17),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )
    
    # Generate binary reference
    binary_id = generate_resource_id("eBinary", f"{patient_id}_docref_{doc_idx}")
    
    doc_ref = {
        "resourceType": "DocumentReference",
        "id": doc_id,
        "extension": [{
            "extension": [
                {
                    "valueCodeableConcept": {
                        "coding": [{
                            "system": "urn:oid:1.2.840.114350.1.72.1.7.7.10.696784.72072",
                            "code": "1",
                            "display": "Signer"
                        }],
                        "text": "Signer"
                    },
                    "url": "mode"
                },
                {
                    "valueDateTime": doc_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "url": "time"
                },
                {
                    "valueReference": {
                        "reference": "Practitioner/ePractitioner123",
                        "display": "Physician, MD"
                    },
                    "url": "party"
                }
            ],
            "url": "http://hl7.org/fhir/5.0/StructureDefinition/extension-DocumentReference.attester"
        }],
        "identifier": [
            {
                "system": "urn:oid:1.2.840.114350.1.13.11511.1.7.2.727879",
                "value": str(500000 + int(hash_val[10:14], 16) % 99999)
            },
            {
                "system": "urn:oid:1.2.840.114350.1.72.3.15",
                "value": f"1.2.840.114350.1.13.11511.1.7.2.727879_{500000 + int(hash_val[10:14], 16) % 99999}"
            }
        ],
        "status": status,
        "docStatus": doc_status,
        "type": {
            "coding": [
                {
                    "system": "urn:oid:1.2.840.114350.1.13.11511.1.7.4.737880.5010",
                    "code": doc_type["code"],
                    "display": doc_type["display"]
                },
                {
                    "system": "http://loinc.org",
                    "code": doc_type["loinc"]["code"],
                    "display": doc_type["loinc"]["display"],
                    "userSelected": True
                }
            ],
            "text": doc_type["text"]
        },
        "category": [{
            "coding": [{
                "system": "http://hl7.org/fhir/us/core/CodeSystem/us-core-documentreference-category",
                "code": category["code"],
                "display": category["display"]
            }],
            "text": category["text"]
        }],
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": patient_name
        },
        "date": doc_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "author": [{
            "reference": "Practitioner/ePractitioner123",
            "type": "Practitioner",
            "display": "Physician, MD"
        }],
        "authenticator": {
            "extension": [{
                "valueDateTime": (doc_date + timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "url": "http://open.epic.com/FHIR/StructureDefinition/extension/clinical-note-authentication-instant"
            }],
            "reference": "Practitioner/ePractitioner123",
            "type": "Practitioner",
            "display": "Physician, MD"
        },
        "custodian": {
            "identifier": {
                "system": "urn:ietf:rfc:3986",
                "value": "urn:epic:cec.fsplyfin"
            },
            "display": "FHIR Playground"
        },
        "content": [
            {
                "attachment": {
                    "contentType": "text/html",
                    "url": f"Binary/{binary_id}"
                },
                "format": {
                    "system": "http://ihe.net/fhir/ValueSet/IHE.FormatCode.codesystem",
                    "code": "urn:ihe:iti:xds:2017:mimeTypeSufficient",
                    "display": "mimeType Sufficient"
                }
            },
            {
                "attachment": {
                    "contentType": "text/rtf",
                    "url": f"Binary/{generate_resource_id('eBinary', f'{patient_id}_docref_{doc_idx}_rtf')}"
                },
                "format": {
                    "system": "http://ihe.net/fhir/ValueSet/IHE.FormatCode.codesystem",
                    "code": "urn:ihe:iti:xds:2017:mimeTypeSufficient",
                    "display": "mimeType Sufficient"
                }
            }
        ],
        "context": {
            "extension": [{
                "valueCodeableConcept": {
                    "coding": [
                        {
                            "system": "urn:oid:1.2.840.114350.1.13.11511.1.7.4.836982.1040",
                            "code": "1",
                            "display": "Physician"
                        },
                        {
                            "system": "urn:oid:2.16.840.1.113883.6.101",
                            "code": "207R00000X",
                            "display": "Internal Medicine Physician"
                        }
                    ],
                    "text": "Physician"
                },
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-documentreference-custodian"
            }],
            "encounter": {
                "reference": f"Encounter/eEnc{hash_val[14:20]}",
                "display": "Office Visit"
            },
            "period": {
                "start": doc_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            },
            "practiceSetting": {
                "coding": [{
                    "system": "urn:oid:1.2.840.114350.1.13.11511.1.7.4.836982.1040",
                    "code": "1",
                    "display": "General Practice"
                }],
                "text": "General Practice"
            }
        }
    }
    
    return doc_ref

def main():
    """Generate consent, binary, and document reference files."""
    # Read patients
    patients_path = Path("Sythetic_Data/patients.json")
    if not patients_path.exists():
        print(f"Error: {patients_path} not found. Please generate patients first.")
        return
    
    with open(patients_path, "r", encoding="utf-8") as f:
        patients = json.load(f)
    
    output_dir = Path("Sythetic_Data")
    output_dir.mkdir(exist_ok=True)
    
    # Generate Consents (Bundle format)
    consent_entries = []
    total_consents = 0
    
    # Generate Binary resources (array format)
    binary_resources = []
    
    # Generate DocumentReferences (array format)
    docref_resources = []
    
    for patient in patients:
        patient_id = patient["id"]
        patient_data = patient.get("data", patient)
        patient_name = get_patient_name(patient)
        
        hash_val = hash_string(patient_id)
        
        # Generate 2-4 consents per patient
        num_consents = (int(hash_val[0:2], 16) % 3) + 2
        for consent_idx in range(num_consents):
            consent_resource = generate_consent(patient_id, patient_name, consent_idx)
            consent_id = consent_resource["id"]
            
            entry = {
                "link": [{
                    "relation": "self",
                    "url": f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Consent/{consent_id}"
                }],
                "fullUrl": f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Consent/{consent_id}",
                "resource": consent_resource,
                "search": {"mode": "match"}
            }
            consent_entries.append(entry)
            total_consents += 1
        
        # Generate 3-6 binary resources per patient
        num_binaries = (int(hash_val[2:4], 16) % 4) + 3
        for binary_idx in range(num_binaries):
            binary_resource = generate_binary(patient_id, binary_idx)
            binary_resources.append(binary_resource)
        
        # Generate 2-5 document references per patient
        num_docs = (int(hash_val[4:6], 16) % 4) + 2
        for doc_idx in range(num_docs):
            docref_resource = generate_document_reference(patient_id, patient_name, doc_idx)
            docref_resources.append(docref_resource)
    
    # Save Consents (Bundle format)
    consent_bundle = {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": total_consents,
        "link": [{
            "relation": "self",
            "url": "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/Consent?patient=*&_count=100"
        }],
        "entry": consent_entries
    }
    
    consent_path = output_dir / "consent.json"
    with open(consent_path, "w", encoding="utf-8") as f:
        json.dump(consent_bundle, f, indent=2, ensure_ascii=False)
    print(f"Generated {total_consents} consents: {consent_path}")
    
    # Save Binary resources (array format)
    binary_path = output_dir / "binary.json"
    with open(binary_path, "w", encoding="utf-8") as f:
        json.dump(binary_resources, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(binary_resources)} binary resources: {binary_path}")
    
    # Save DocumentReferences (array format)
    docref_path = output_dir / "docref.json"
    with open(docref_path, "w", encoding="utf-8") as f:
        json.dump(docref_resources, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(docref_resources)} document references: {docref_path}")

if __name__ == "__main__":
    main()

