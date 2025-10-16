# backend/app/api/v1/patients.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.patient import PatientCreate, PatientResponse, PatientAPIResponse
from app.services.patient_service import patient as patient_service

router = APIRouter()


@router.get("/", response_model=List[PatientAPIResponse])  # Use the new response model
def read_patients(
    db: Session = Depends(deps.get_db),
):
    """
    Retrieve all patients.
    """
    patients = patient_service.get_multi(db=db)
    # For each patient, construct the new response object
    return [
        {"id": p.id, "fhir_resource": PatientResponse.parse_obj(p.fhir_resource)}
        for p in patients
    ]


@router.post("/", response_model=PatientResponse)
def create_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_in: PatientCreate,
):
    """
    Create a new patient using a FHIR Patient resource.
    """
    patient = patient_service.create(db=db, obj_in=patient_in)
    return PatientResponse.parse_obj(patient.fhir_resource)


@router.get("/{patient_id}", response_model=PatientResponse)
def read_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_id: int,
):
    """
    Retrieve a patient by ID.
    """
    patient = patient_service.get_by_id(db=db, patient_id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return PatientResponse.parse_obj(patient.fhir_resource)
