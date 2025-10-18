# backend/app/models/note.py
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    summary = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="notes")
