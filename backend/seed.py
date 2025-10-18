# backend/seed.py
import logging
from app.db.session import SessionLocal
from app.services.user_service import user as user_service
from app.services.patient_service import patient as patient_service
from app.services.note_service import note as note_service
from app.schemas.user import UserCreate
from app.schemas.patient import PatientCreate
from app.schemas.note import NoteCreate
from app.models.patient import Patient  # Import the Patient model for type hinting

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_data():
    db = SessionLocal()
    try:
        # Create a User
        user_in = UserCreate(email="test@example.com", password="password123")
        user = user_service.get_by_email(db, email=user_in.email)
        if not user:
            user = user_service.create(db, obj_in=user_in)
            logger.info(f"User '{user.email}' created.")
        else:
            logger.info(f"User '{user.email}' already exists.")

        # Create a Patient
        # A simple check to avoid creating duplicate patients in this script
        existing_patient = patient_service.get(db, id=1)
        if not existing_patient:
            patient_in = PatientCreate(
                resourceType="Patient",
                name=[{"family": "Smith", "given": ["John", "B."]}],
                gender="male",
                birthDate="1974-12-25",
            )
            patient: Patient = patient_service.create(db, obj_in=patient_in)
            logger.info(f"Patient 'John B. Smith' with ID {patient.id} created.")

            # This check ensures patient.id is not None for the type checker
            if patient.id is not None:
                # Explicitly cast to int to satisfy linters
                patient_id = int(patient.id)

                # Create a Note for the Patient
                note_in = NoteCreate(
                    content=(
                        "Patient presents today for a routine check-up. "
                        "No new complaints."
                    ),
                    patient_id=patient_id,
                )
                note = note_service.create(db, obj_in=note_in)
                logger.info(f"Note with ID {note.id} created for patient {patient.id}.")
        else:
            logger.info("Patient 'John B. Smith' already exists.")

        logger.info("Database seeding finished.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
