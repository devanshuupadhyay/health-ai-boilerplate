# backend/app/services/patient_service.py
from typing import Optional, Any, Type, List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder  # <--- IMPORT THIS
from app.models.patient import Patient
from app.schemas.patient import PatientCreate


class PatientService:
    def __init__(self, model: Type[Patient]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[Patient]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session) -> List[Patient]:
        return db.query(self.model).all()

    def create(self, db: Session, *, obj_in: PatientCreate) -> Patient:
        # Use jsonable_encoder to correctly handle date/datetime objects
        fhir_resource_dict = jsonable_encoder(obj_in)  # <--- CHANGE THIS LINE

        # The rest of the function remains the same
        family_name = None
        given_name = None
        if obj_in.name and obj_in.name[0]:
            family_name = obj_in.name[0].family
            if obj_in.name[0].given:
                given_name = " ".join(obj_in.name[0].given)

        birth_date = obj_in.birthDate

        db_obj = Patient(
            fhir_resource=fhir_resource_dict,
            family_name=family_name,
            given_name=given_name,
            birth_date=birth_date,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_id(self, db: Session, *, patient_id: int) -> Optional[Patient]:
        return db.query(self.model).filter(self.model.id == patient_id).first()


patient = PatientService(Patient)
