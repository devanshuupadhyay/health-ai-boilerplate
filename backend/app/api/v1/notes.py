# backend/app/api/v1/notes.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.note import Note, NoteCreate
from app.services.note_service import note as note_service
from app.services.patient_service import patient as patient_service

router = APIRouter()


@router.post("/", response_model=Note)
def create_note(
    *,
    db: Session = Depends(deps.get_db),
    note_in: NoteCreate,
):
    """
    Create a new note for a patient.
    """
    # Verify patient exists before creating a note
    patient = patient_service.get(db=db, id=note_in.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    note = note_service.create(db=db, obj_in=note_in)
    return note


@router.get("/patient/{patient_id}", response_model=List[Note])
def read_notes_by_patient(
    *,
    db: Session = Depends(deps.get_db),
    patient_id: int,
):
    """
    Retrieve all notes for a specific patient.
    """
    notes = note_service.get_notes_by_patient(db=db, patient_id=patient_id)
    return notes
