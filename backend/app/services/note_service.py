# backend/app/services/note_service.py
from typing import List, Optional, Any, Type
from sqlalchemy.orm import Session
from app.models.note import Note
from app.schemas.note import NoteCreate
from celery_worker import celery


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
        db.refresh(db_obj)

        # Trigger the background task by its string name to avoid circular imports
        if db_obj.id:
            celery.send_task(
                "app.tasks.process_note.summarize_note_task", args=[db_obj.id]
            )

        return db_obj

    def get_notes_by_patient(self, db: Session, *, patient_id: int) -> List[Note]:
        """
        Get all notes for a specific patient.
        """
        return db.query(self.model).filter(self.model.patient_id == patient_id).all()


note = NoteService(Note)
