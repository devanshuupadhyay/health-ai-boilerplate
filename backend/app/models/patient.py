# backend/app/models/patient.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects.postgresql import JSONB
from app.db.session import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    # Store the full FHIR resource as JSON for compliance and flexibility
    fhir_resource = Column(JSONB, nullable=False)

    # Add specific, indexed columns for fields that need to be queried frequently
    # This is a practical approach for performance.
    family_name = Column(String, index=True, nullable=True)
    given_name = Column(String, index=True, nullable=True)
    birth_date = Column(Date, nullable=True)
