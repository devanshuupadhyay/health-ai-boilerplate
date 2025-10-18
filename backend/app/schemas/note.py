# backend/app/schemas/note.py
from pydantic import BaseModel
from typing import Optional  # <-- IMPORT Optional


class NoteBase(BaseModel):
    content: str
    patient_id: int


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    summary: Optional[str] = None

    class Config:
        from_attributes = True
