"""
FastAPI service for serving synthetic FHIR R4 data
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pathlib import Path
import json
from typing import Optional, List, Dict, Any
import re
from datetime import datetime, date

app = FastAPI(
    title="GooClaim FHIR Mock API",
    description="Synthetic FHIR R4 test data API - Epic Compatible",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Data directory
DATA_DIR = Path("Sythetic_Data")

# Load all data files
def load_data():
    """Load all synthetic data files"""
    data = {}
    
    # Patient data (array format)
    patients_file = DATA_DIR / "patients.json"
    if patients_file.exists():
        with open(patients_file, "r", encoding="utf-8") as f:
            data["Patient"] = json.load(f)
    
    # Organization data (array format)
    org_file = DATA_DIR / "organisation.json"
    if org_file.exists():
        with open(org_file, "r", encoding="utf-8") as f:
            data["Organization"] = json.load(f)
    
    # Coverage data (object with coverage array)
    coverage_file = DATA_DIR / "coverage.json"
    if coverage_file.exists():
        with open(coverage_file, "r", encoding="utf-8") as f:
            coverage_data = json.load(f)
            data["Coverage"] = coverage_data.get("coverage", [])
    
    # Practitioner data (array format)
    practitioner_file = DATA_DIR / "practitioner.json"
    if practitioner_file.exists():
        with open(practitioner_file, "r", encoding="utf-8") as f:
            data["Practitioner"] = json.load(f)
    
    # PractitionerRole data (array format)
    practitioner_role_file = DATA_DIR / "practitonerrole.json"
    if practitioner_role_file.exists():
        with open(practitioner_role_file, "r", encoding="utf-8") as f:
            data["PractitionerRole"] = json.load(f)
    
    # Bundle resources (Encounter, Procedure, Condition, Consent)
    bundle_resources = {
        "Encounter": "encounterr.json",
        "Procedure": "procedure.json",
        "Condition": "conditionss.json",
        "Consent": "consent.json"
    }
    
    for resource_type, filename in bundle_resources.items():
        file_path = DATA_DIR / filename
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                bundle = json.load(f)
                if isinstance(bundle, dict) and "entry" in bundle:
                    # Extract resources from bundle entries
                    data[resource_type] = [entry.get("resource", {}) for entry in bundle.get("entry", [])]
                else:
                    data[resource_type] = []
    
    # Array resources (Observation, DocumentReference, Binary, Provenance)
    array_resources = {
        "Observation": "observation.json",
        "DocumentReference": "docref.json",
        "Binary": "binary.json",
        "Provenance": "provenance.json"
    }
    
    for resource_type, filename in array_resources.items():
        file_path = DATA_DIR / filename
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                data[resource_type] = json.load(f)
    
    # EOB (Bundle with OperationOutcome)
    eob_file = DATA_DIR / "eob.json"
    if eob_file.exists():
        with open(eob_file, "r", encoding="utf-8") as f:
            data["ExplanationOfBenefit"] = json.load(f)
    
    # Appointment data (custom format with appointments array)
    appointment_file = DATA_DIR / "appointments.json"
    if appointment_file.exists():
        with open(appointment_file, "r", encoding="utf-8") as f:
            appointment_data = json.load(f)
            # Extract full_resource from each appointment
            appointments = appointment_data.get("appointments", [])
            data["Appointment"] = [apt.get("full_resource", {}) for apt in appointments if apt.get("full_resource")]
    
    return data

# Load data on startup
FHIR_DATA = load_data()

def get_resource_by_id(resource_type: str, resource_id: str) -> Optional[Dict]:
    """Get a resource by ID"""
    resources = FHIR_DATA.get(resource_type, [])
    
    for resource in resources:
        if isinstance(resource, dict):
            # Handle wrapped Patient resources
            if resource_type == "Patient" and "data" in resource:
                if resource.get("id") == resource_id or resource.get("data", {}).get("id") == resource_id:
                    return resource
            # Handle regular resources
            elif resource.get("id") == resource_id:
                return resource
    
    return None

def search_resources(resource_type: str, filters: Dict[str, Any]) -> List[Dict]:
    """Search resources with filters"""
    resources = FHIR_DATA.get(resource_type, [])
    results = []
    
    for resource in resources:
        if not isinstance(resource, dict):
            continue
        
        match = True
        
        # Patient filter
        if "patient" in filters:
            patient_id = filters["patient"]
            # Check subject.reference, patient.reference, or beneficiary
            subject_ref = resource.get("subject", {}).get("reference", "")
            patient_ref = resource.get("patient", {}).get("reference", "")
            beneficiary_ref = resource.get("beneficiary", "")
            
            if isinstance(beneficiary_ref, str):
                beneficiary_id = beneficiary_ref.replace("Patient/", "")
            else:
                beneficiary_id = beneficiary_ref.get("reference", "").replace("Patient/", "") if isinstance(beneficiary_ref, dict) else ""
            
            patient_id_check = patient_id.replace("Patient/", "")
            
            if (f"Patient/{patient_id_check}" not in subject_ref and 
                f"Patient/{patient_id_check}" not in patient_ref and
                patient_id_check != beneficiary_id):
                match = False
        
        # Organization filter
        if "organization" in filters and match:
            org_id = filters["organization"].replace("Organization/", "")
            service_provider = resource.get("serviceProvider", {}).get("reference", "")
            payor_refs = resource.get("payor", [])
            
            if isinstance(payor_refs, list):
                payor_match = any(f"Organization/{org_id}" in payor.get("reference", "") for payor in payor_refs)
            else:
                payor_match = False
            
            if f"Organization/{org_id}" not in service_provider and not payor_match:
                match = False
        
        if match:
            results.append(resource)
    
    return results

def create_bundle_response(resources: List[Dict], resource_type: str, total: Optional[int] = None) -> Dict:
    """Create a FHIR Bundle response"""
    if total is None:
        total = len(resources)
    
    entries = []
    for resource in resources:
        resource_id = resource.get("id", "")
        entries.append({
            "fullUrl": f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/{resource_type}/{resource_id}",
            "resource": resource,
            "search": {
                "mode": "match"
            }
        })
    
    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": total,
        "link": [{
            "relation": "self",
            "url": f"https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/{resource_type}?_count=100"
        }],
        "entry": entries
    }

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "GooClaim FHIR Mock API",
        "version": "1.0.0",
        "resources": list(FHIR_DATA.keys())
    }

# Patient endpoints
@app.get("/Patient/{patient_id}")
def get_patient(patient_id: str):
    """Get a specific patient by ID - Epic compatible format"""
    patient = get_resource_by_id("Patient", patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    # Return patient with wrapper structure (matches Epic format)
    return patient

@app.get("/Patient")
def search_patients(
    _id: Optional[str] = Query(None, description="Patient ID"),
    identifier: Optional[str] = Query(None, description="Identifier value"),
    name: Optional[str] = Query(None, description="Patient name"),
    family: Optional[str] = Query(None, description="Family name"),
    given: Optional[str] = Query(None, description="Given name"),
    birthdate: Optional[str] = Query(None, description="Birth date"),
    gender: Optional[str] = Query(None, description="Gender"),
    _count: Optional[int] = Query(None, description="Number of results")
):
    """Search for patients - Epic compatible"""
    patients = FHIR_DATA.get("Patient", [])
    filtered = []
    
    for patient in patients:
        match = True
        patient_data = patient.get("data", patient)
        
        # Filter by _id
        if _id and patient.get("id") != _id:
            match = False
        
        # Filter by identifier
        if identifier and match:
            identifiers = patient_data.get("identifier", [])
            ident_match = any(ident.get("value") == identifier for ident in identifiers)
            if not ident_match:
                match = False
        
        # Filter by family name
        if family and match:
            names = patient_data.get("name", [])
            family_match = any(family.lower() in name.get("family", "").lower() for name in names)
            if not family_match:
                match = False
        
        # Filter by given name
        if given and match:
            names = patient_data.get("name", [])
            given_match = any(given.lower() in " ".join(name.get("given", [])).lower() for name in names)
            if not given_match:
                match = False
        
        # Filter by name (full name search)
        if name and match:
            names = patient_data.get("name", [])
            name_match = any(name.lower() in (name_obj.get("text", "") or 
                                              f"{' '.join(name_obj.get('given', []))} {name_obj.get('family', '')}").lower() 
                             for name_obj in names)
            if not name_match:
                match = False
        
        # Filter by birthdate
        if birthdate and match:
            if patient_data.get("birthDate") != birthdate:
                match = False
        
        # Filter by gender
        if gender and match:
            if patient_data.get("gender") != gender:
                match = False
        
        if match:
            filtered.append(patient)
    
    # Limit results
    if _count:
        filtered = filtered[:_count]
    
    return create_bundle_response(filtered, "Patient")

# Organization endpoints
@app.get("/Organization/{org_id}")
def get_organization(org_id: str):
    """Get a specific organization by ID"""
    org = get_resource_by_id("Organization", org_id)
    if not org:
        raise HTTPException(status_code=404, detail=f"Organization {org_id} not found")
    return org

@app.get("/Organization")
def search_organizations(_count: Optional[int] = Query(None)):
    """Search for organizations"""
    orgs = FHIR_DATA.get("Organization", [])
    if _count:
        orgs = orgs[:_count]
    return create_bundle_response(orgs, "Organization")

# Coverage endpoints
@app.get("/Coverage/{coverage_id}")
def get_coverage(coverage_id: str):
    """Get a specific coverage by ID"""
    coverage = get_resource_by_id("Coverage", coverage_id)
    if not coverage:
        raise HTTPException(status_code=404, detail=f"Coverage {coverage_id} not found")
    return coverage

@app.get("/Coverage")
def search_coverages(
    patient: Optional[str] = Query(None, description="Patient ID"),
    beneficiary: Optional[str] = Query(None, description="Beneficiary ID"),
    _count: Optional[int] = Query(None)
):
    """Search for coverage"""
    filters = {}
    if patient:
        filters["patient"] = patient
    if beneficiary:
        filters["patient"] = beneficiary
    
    coverages = search_resources("Coverage", filters) if filters else FHIR_DATA.get("Coverage", [])
    if _count:
        coverages = coverages[:_count]
    
    return create_bundle_response(coverages, "Coverage")

# Encounter endpoints
@app.get("/Encounter/{encounter_id}")
def get_encounter(encounter_id: str):
    """Get a specific encounter by ID"""
    encounter = get_resource_by_id("Encounter", encounter_id)
    if not encounter:
        raise HTTPException(status_code=404, detail=f"Encounter {encounter_id} not found")
    return encounter

@app.get("/Encounter")
def search_encounters(
    _id: Optional[str] = Query(None, description="Encounter ID"),
    patient: Optional[str] = Query(None, description="Patient ID"),
    organization: Optional[str] = Query(None, description="Organization ID"),
    status: Optional[str] = Query(None, description="Encounter status"),
    class_code: Optional[str] = Query(None, alias="class", description="Encounter class"),
    date: Optional[str] = Query(None, description="Date filter"),
    _count: Optional[int] = Query(None)
):
    """Search for encounters - Epic compatible"""
    filters = {}
    if patient:
        filters["patient"] = patient
    if organization:
        filters["organization"] = organization
    
    encounters = search_resources("Encounter", filters) if filters else FHIR_DATA.get("Encounter", [])
    
    # Additional filters
    filtered = []
    for enc in encounters:
        match = True
        
        # Filter by _id
        if _id and enc.get("id") != _id:
            match = False
        
        # Filter by status
        if status and match:
            if enc.get("status") != status:
                match = False
        
        # Filter by class
        if class_code and match:
            enc_class = enc.get("class", {}).get("code", "")
            if enc_class != class_code:
                match = False
        
        # Filter by date
        if date and match:
            period_start = enc.get("period", {}).get("start", "")
            if date not in period_start:
                match = False
        
        if match:
            filtered.append(enc)
    
    if _count:
        filtered = filtered[:_count]
    
    return create_bundle_response(filtered, "Encounter", total=len(filtered))

# Condition endpoints
@app.get("/Condition/{condition_id}")
def get_condition(condition_id: str):
    """Get a specific condition by ID"""
    condition = get_resource_by_id("Condition", condition_id)
    if not condition:
        raise HTTPException(status_code=404, detail=f"Condition {condition_id} not found")
    return condition

@app.get("/Condition")
def search_conditions(
    _id: Optional[str] = Query(None, description="Condition ID"),
    patient: Optional[str] = Query(None, description="Patient ID"),
    clinical_status: Optional[str] = Query(None, alias="clinical-status", description="Clinical status"),
    category: Optional[str] = Query(None, description="Category"),
    code: Optional[str] = Query(None, description="Condition code"),
    _count: Optional[int] = Query(None)
):
    """Search for conditions - Epic compatible"""
    filters = {}
    if patient:
        filters["patient"] = patient
    
    conditions = search_resources("Condition", filters) if filters else FHIR_DATA.get("Condition", [])
    
    # Additional filters
    filtered = []
    for condition in conditions:
        match = True
        
        # Filter by _id
        if _id and condition.get("id") != _id:
            match = False
        
        # Filter by clinical-status
        if clinical_status and match:
            status = condition.get("clinicalStatus", {}).get("coding", [{}])[0].get("code", "")
            if status != clinical_status:
                match = False
        
        # Filter by category
        if category and match:
            categories = condition.get("category", [])
            cat_match = any(cat.get("coding", [{}])[0].get("code", "") == category for cat in categories)
            if not cat_match:
                match = False
        
        # Filter by code
        if code and match:
            codes = condition.get("code", {}).get("coding", [])
            code_match = any(c.get("code", "") == code for c in codes)
            if not code_match:
                match = False
        
        if match:
            filtered.append(condition)
    
    if _count:
        filtered = filtered[:_count]
    
    return create_bundle_response(filtered, "Condition", total=len(filtered))

# Procedure endpoints
@app.get("/Procedure/{procedure_id}")
def get_procedure(procedure_id: str):
    """Get a specific procedure by ID"""
    procedure = get_resource_by_id("Procedure", procedure_id)
    if not procedure:
        raise HTTPException(status_code=404, detail=f"Procedure {procedure_id} not found")
    return procedure

@app.get("/Procedure")
def search_procedures(
    _id: Optional[str] = Query(None, description="Procedure ID"),
    patient: Optional[str] = Query(None, description="Patient ID"),
    date: Optional[str] = Query(None, description="Date filter"),
    status: Optional[str] = Query(None, description="Procedure status"),
    _count: Optional[int] = Query(None)
):
    """Search for procedures - Epic compatible"""
    filters = {}
    if patient:
        filters["patient"] = patient
    
    procedures = search_resources("Procedure", filters) if filters else FHIR_DATA.get("Procedure", [])
    
    # Additional filters
    filtered = []
    for proc in procedures:
        match = True
        
        # Filter by _id
        if _id and proc.get("id") != _id:
            match = False
        
        # Filter by status
        if status and match:
            if proc.get("status") != status:
                match = False
        
        # Filter by date
        if date and match:
            performed_date = proc.get("performedDateTime", "")
            if date not in performed_date:
                match = False
        
        if match:
            filtered.append(proc)
    
    if _count:
        filtered = filtered[:_count]
    
    return create_bundle_response(filtered, "Procedure", total=len(filtered))

# Observation endpoints
@app.get("/Observation/{observation_id}")
def get_observation(observation_id: str):
    """Get a specific observation by ID"""
    observation = get_resource_by_id("Observation", observation_id)
    if not observation:
        raise HTTPException(status_code=404, detail=f"Observation {observation_id} not found")
    return observation

@app.get("/Observation")
def search_observations(
    _id: Optional[str] = Query(None, description="Observation ID"),
    patient: Optional[str] = Query(None, description="Patient ID"),
    encounter: Optional[str] = Query(None, description="Encounter ID"),
    category: Optional[str] = Query(None, description="Category (e.g., vital-signs, laboratory)"),
    code: Optional[str] = Query(None, description="Observation code"),
    date: Optional[str] = Query(None, description="Date filter"),
    _count: Optional[int] = Query(None)
):
    """Search for observations - Epic compatible (requires category or code)"""
    filters = {}
    if patient:
        filters["patient"] = patient
    
    observations = search_resources("Observation", filters) if filters else FHIR_DATA.get("Observation", [])
    
    # Epic requires category or code parameter
    if not category and not code and not patient:
        raise HTTPException(
            status_code=400, 
            detail="At least one of category, code, or patient parameter is required"
        )
    
    # Additional filters
    filtered = []
    for obs in observations:
        match = True
        
        # Filter by _id
        if _id and obs.get("id") != _id:
            match = False
        
        # Filter by encounter
        if encounter and match:
            encounter_id = encounter.replace("Encounter/", "")
            if obs.get("encounter", {}).get("reference", "").replace("Encounter/", "") != encounter_id:
                match = False
        
        # Filter by category
        if category and match:
            categories = obs.get("category", [])
            cat_match = any(cat.get("coding", [{}])[0].get("code", "") == category for cat in categories)
            if not cat_match:
                match = False
        
        # Filter by code
        if code and match:
            codes = obs.get("code", {}).get("coding", [])
            code_match = any(c.get("code", "") == code for c in codes)
            if not code_match:
                match = False
        
        # Filter by date
        if date and match:
            effective_date = obs.get("effectiveDateTime", "")
            if date not in effective_date:
                match = False
        
        if match:
            filtered.append(obs)
    
    if _count:
        filtered = filtered[:_count]
    
    return create_bundle_response(filtered, "Observation", total=len(filtered))

# Practitioner endpoints
@app.get("/Practitioner/{practitioner_id}")
def get_practitioner(practitioner_id: str):
    """Get a specific practitioner by ID"""
    practitioner = get_resource_by_id("Practitioner", practitioner_id)
    if not practitioner:
        raise HTTPException(status_code=404, detail=f"Practitioner {practitioner_id} not found")
    return practitioner

@app.get("/Practitioner")
def search_practitioners(_count: Optional[int] = Query(None)):
    """Search for practitioners"""
    practitioners = FHIR_DATA.get("Practitioner", [])
    if _count:
        practitioners = practitioners[:_count]
    return create_bundle_response(practitioners, "Practitioner")

# PractitionerRole endpoints
@app.get("/PractitionerRole/{role_id}")
def get_practitioner_role(role_id: str):
    """Get a specific practitioner role by ID"""
    role = get_resource_by_id("PractitionerRole", role_id)
    if not role:
        raise HTTPException(status_code=404, detail=f"PractitionerRole {role_id} not found")
    return role

@app.get("/PractitionerRole")
def search_practitioner_roles(
    practitioner: Optional[str] = Query(None, description="Practitioner ID"),
    _count: Optional[int] = Query(None)
):
    """Search for practitioner roles"""
    roles = FHIR_DATA.get("PractitionerRole", [])
    
    if practitioner:
        practitioner_id = practitioner.replace("Practitioner/", "")
        roles = [
            role for role in roles 
            if role.get("practitioner", {}).get("reference", "").replace("Practitioner/", "") == practitioner_id
        ]
    
    if _count:
        roles = roles[:_count]
    
    return create_bundle_response(roles, "PractitionerRole")

# DocumentReference endpoints
@app.get("/DocumentReference/{doc_id}")
def get_document_reference(doc_id: str):
    """Get a specific document reference by ID"""
    doc = get_resource_by_id("DocumentReference", doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail=f"DocumentReference {doc_id} not found")
    return doc

@app.get("/DocumentReference")
def search_document_references(
    _id: Optional[str] = Query(None, description="DocumentReference ID"),
    patient: Optional[str] = Query(None, description="Patient ID"),
    status: Optional[str] = Query(None, description="Status"),
    date: Optional[str] = Query(None, description="Date filter"),
    type: Optional[str] = Query(None, description="Document type"),
    _count: Optional[int] = Query(None)
):
    """Search for document references - Epic compatible"""
    filters = {}
    if patient:
        filters["patient"] = patient
    
    docs = search_resources("DocumentReference", filters) if filters else FHIR_DATA.get("DocumentReference", [])
    
    # Additional filters
    filtered = []
    for doc in docs:
        match = True
        
        # Filter by _id
        if _id and doc.get("id") != _id:
            match = False
        
        # Filter by status
        if status and match:
            if doc.get("status") != status:
                match = False
        
        # Filter by date
        if date and match:
            doc_date = doc.get("date", "")
            if date not in doc_date:
                match = False
        
        # Filter by type
        if type and match:
            doc_types = doc.get("type", {}).get("coding", [])
            type_match = any(t.get("code", "") == type for t in doc_types)
            if not type_match:
                match = False
        
        if match:
            filtered.append(doc)
    
    if _count:
        filtered = filtered[:_count]
    
    return create_bundle_response(filtered, "DocumentReference", total=len(filtered))

# Consent endpoints
@app.get("/Consent/{consent_id}")
def get_consent(consent_id: str):
    """Get a specific consent by ID"""
    consent = get_resource_by_id("Consent", consent_id)
    if not consent:
        raise HTTPException(status_code=404, detail=f"Consent {consent_id} not found")
    return consent

@app.get("/Consent")
def search_consents(
    _id: Optional[str] = Query(None, description="Consent ID"),
    patient: Optional[str] = Query(None, description="Patient ID"),
    status: Optional[str] = Query(None, description="Status"),
    category: Optional[str] = Query(None, description="Category"),
    _count: Optional[int] = Query(None)
):
    """Search for consents - Epic compatible"""
    filters = {}
    if patient:
        filters["patient"] = patient
    
    consents = search_resources("Consent", filters) if filters else FHIR_DATA.get("Consent", [])
    
    # Additional filters
    filtered = []
    for consent in consents:
        match = True
        
        # Filter by _id
        if _id and consent.get("id") != _id:
            match = False
        
        # Filter by status
        if status and match:
            if consent.get("status") != status:
                match = False
        
        # Filter by category
        if category and match:
            categories = consent.get("category", [])
            cat_match = any(cat.get("coding", [{}])[0].get("code", "") == category for cat in categories)
            if not cat_match:
                match = False
        
        if match:
            filtered.append(consent)
    
    if _count:
        filtered = filtered[:_count]
    
    return create_bundle_response(filtered, "Consent", total=len(filtered))

# Binary endpoints
@app.get("/Binary/{binary_id}")
def get_binary(binary_id: str):
    """Get a specific binary resource by ID"""
    binary = get_resource_by_id("Binary", binary_id)
    if not binary:
        raise HTTPException(status_code=404, detail=f"Binary {binary_id} not found")
    return binary

# Provenance endpoints
@app.get("/Provenance/{provenance_id}")
def get_provenance(provenance_id: str):
    """Get a specific provenance by ID"""
    provenance = get_resource_by_id("Provenance", provenance_id)
    if not provenance:
        raise HTTPException(status_code=404, detail=f"Provenance {provenance_id} not found")
    return provenance

@app.get("/Provenance")
def search_provenance(
    target: Optional[str] = Query(None, description="Target resource reference"),
    _count: Optional[int] = Query(None)
):
    """Search for provenance"""
    provenances = FHIR_DATA.get("Provenance", [])
    
    if target:
        provenances = [
            prov for prov in provenances 
            if any(target in t.get("reference", "") for t in prov.get("target", []))
        ]
    
    if _count:
        provenances = provenances[:_count]
    
    return create_bundle_response(provenances, "Provenance", total=len(provenances))

# ExplanationOfBenefit endpoint
@app.get("/ExplanationOfBenefit")
def search_eob(
    patient: Optional[str] = Query(None, description="Patient ID"),
    _count: Optional[int] = Query(None)
):
    """Search for ExplanationOfBenefit (returns OperationOutcome)"""
    # Return the EOB bundle (which contains OperationOutcome)
    return FHIR_DATA.get("ExplanationOfBenefit", {})

# Appointment endpoints
@app.get("/Appointment/{appointment_id}")
def get_appointment(appointment_id: str):
    """Get a specific appointment by ID"""
    appointment = get_resource_by_id("Appointment", appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail=f"Appointment {appointment_id} not found")
    return appointment

@app.get("/Appointment")
def search_appointments(
    _id: Optional[str] = Query(None, description="Appointment ID"),
    patient: Optional[str] = Query(None, description="Patient ID"),
    status: Optional[str] = Query(None, description="Appointment status"),
    date: Optional[str] = Query(None, description="Date filter - Epic standard: 'ge2025-01-01', 'le2025-12-31', 'eq2025-11-05', 'gt2025-01-01', 'lt2025-12-31', or partial '2025-11'"),
    actor: Optional[str] = Query(None, description="Actor (Patient/Practitioner/Location)"),
    _count: Optional[int] = Query(None)
):
    """
    Search for appointments - Epic compatible
    
    Epic Scope: Appointment.Read (Appointments) (R4), Appointment.Search (Appointments) (R4)
    Epic Parameters: _id, patient, status, date, actor, _count
    Date Format: Epic standard FHIR (eqYYYY-MM-DD, geYYYY-MM-DD, leYYYY-MM-DD, gtYYYY-MM-DD, ltYYYY-MM-DD)
    """
    filters = {}
    if patient:
        filters["patient"] = patient
    
    appointments = search_resources("Appointment", filters) if filters else FHIR_DATA.get("Appointment", [])
    
    # Additional filters
    filtered = []
    for apt in appointments:
        match = True
        
        # Filter by _id
        if _id and apt.get("id") != _id:
            match = False
        
        # Filter by status
        if status and match:
            if apt.get("status") != status:
                match = False
        
        # Filter by date (Epic supports date prefixes: ge, le, gt, lt, eq, and "today")
        if date and match:
            start_date_str = apt.get("start", "")
            if not start_date_str:
                match = False
            else:
                # Parse appointment start date
                try:
                    # Handle ISO format: 2025-11-05T14:00:00Z
                    if "T" in start_date_str:
                        apt_date = datetime.fromisoformat(start_date_str.replace("Z", "+00:00")).date()
                    else:
                        apt_date = datetime.fromisoformat(start_date_str).date()
                    
                    # Handle date parameter (Epic standard FHIR format: ge2025-01-01, le2025-12-31, eq2025-11-05)
                    # Note: Epic does NOT support "today" - only standard FHIR prefixes
                    date_param = date.lower().strip()
                    
                    # Epic standard: date=eqYYYY-MM-DD, date=geYYYY-MM-DD, date=leYYYY-MM-DD, etc.
                    if date_param.startswith(("ge", "le", "gt", "lt", "eq")):
                        # Handle FHIR date prefixes
                        prefix = date_param[:2]
                        date_str = date_param[2:]
                        
                        try:
                            filter_date = datetime.fromisoformat(date_str).date()
                            
                            if prefix == "ge":  # greater than or equal
                                if apt_date < filter_date:
                                    match = False
                            elif prefix == "le":  # less than or equal
                                if apt_date > filter_date:
                                    match = False
                            elif prefix == "gt":  # greater than
                                if apt_date <= filter_date:
                                    match = False
                            elif prefix == "lt":  # less than
                                if apt_date >= filter_date:
                                    match = False
                            elif prefix == "eq":  # equals
                                if apt_date != filter_date:
                                    match = False
                        except:
                            # Fallback to simple string matching
                            if date_str not in start_date_str:
                                match = False
                    else:
                        # Simple string matching (for partial dates like "2025-11")
                        if date not in start_date_str:
                            match = False
                except:
                    # Fallback to simple string matching
                    if date not in start_date_str:
                        match = False
        
        # Filter by actor
        if actor and match:
            participants = apt.get("participant", [])
            actor_match = any(actor in p.get("actor", {}).get("reference", "") for p in participants)
            if not actor_match:
                match = False
        
        if match:
            filtered.append(apt)
    
    if _count:
        filtered = filtered[:_count]
    
    return create_bundle_response(filtered, "Appointment", total=len(filtered))

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "resources_loaded": len(FHIR_DATA),
        "resource_types": list(FHIR_DATA.keys())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

