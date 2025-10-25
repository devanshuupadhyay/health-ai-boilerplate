# backend/app/services/note_service.py
from typing import List, Optional, Any, Type
from sqlalchemy.orm import Session
from app.models.note import Note
from app.schemas.note import NoteCreate
from celery_worker import celery

# --- ADD THIS IMPORT ---
from app.core.logging_config import get_logger

# --- END IMPORT ---

# --- Use Structlog logger ---
log = get_logger(__name__)
# --- END ---


class NoteService:
    def __init__(self, model: Type[Note]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[Note]:
        """
        Get a note by its ID.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: NoteCreate) -> Note:
        """
        Create a new note and trigger a background task for summarization.
        """
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)  # Refresh the object to get the generated ID

        # --- MOVE & MODIFY THE CELERY TRIGGER ---
        # Now db_obj.id definitely has the integer value (or None if refresh failed)
        if db_obj.id is not None:
            try:
                celery.send_task(
                    "app.tasks.process_note.summarize_note_task", args=[db_obj.id]
                )
                log.info("Celery summarize task sent", note_id=db_obj.id)  # Use logger
            except Exception as e:
                # Log if sending the task fails, but don't crash the request
                log.error(
                    "Failed to send Celery summarize task",
                    note_id=db_obj.id,
                    error=str(e),
                    exc_info=True,
                )
        else:
            # This case is unlikely if commit/refresh succeeded, but good to handle
            log.error(
                "Note created but ID not available after refresh",
                patient_id=obj_in.patient_id,
            )
        # --- END MOVE & MODIFY ---

        return db_obj

    def get_notes_by_patient(self, db: Session, *, patient_id: int) -> List[Note]:
        """
        Get all notes for a specific patient.
        """
        return (
            db.query(self.model)
            .filter(self.model.patient_id == patient_id)
            .order_by(self.model.id.desc())
            .all()
        )


note = NoteService(Note)
