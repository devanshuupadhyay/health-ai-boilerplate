# backend/app/models/patient.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.session import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    fhir_resource = Column(JSONB, nullable=False)
    family_name = Column(String, index=True, nullable=True)
    given_name = Column(String, index=True, nullable=True)
    birth_date = Column(Date, nullable=True)

    notes = relationship("Note", back_populates="patient")
