# backend/app/api/v1/notes.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.note import Note, NoteCreate  # Ensure Note is imported from schemas
from app.services.note_service import note as note_service
from app.services.patient_service import patient as patient_service
import logging  # <-- ADD THIS IMPORT

router = APIRouter()
logger = logging.getLogger(__name__)  # <-- ADD LOGGER INSTANCE


@router.post("/", response_model=Note)
def create_note(
    *,
    db: Session = Depends(deps.get_db),
    note_in: NoteCreate,
):
    """
    Create a new note for a patient.
    """
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

    # --- ADD THIS LOGGING LOOP ---
    logger.info(f"Fetched {len(notes)} notes from service for patient {patient_id}.")
    for note_obj in notes:
        logger.info(
            f"Note ID: {note_obj.id}, Summary from DB object: {note_obj.summary}"
        )
    # --- END LOGGING LOOP ---

    return notes
