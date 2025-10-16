# backend/app/schemas/patient.py
from pydantic import BaseModel
from fhir.resources.patient import Patient as FHIRPatient


class PatientCreate(FHIRPatient):
    pass


PatientResponse = FHIRPatient


# --- ADD THIS NEW CLASS ---
class PatientAPIResponse(BaseModel):
    id: int
    fhir_resource: PatientResponse


# --- END OF NEW CLASS ---
