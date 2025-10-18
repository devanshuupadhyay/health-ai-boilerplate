# backend/app/schemas/note.py
from pydantic import BaseModel


class NoteBase(BaseModel):
    content: str
    patient_id: int


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int

    class Config:
        from_attributes = True
