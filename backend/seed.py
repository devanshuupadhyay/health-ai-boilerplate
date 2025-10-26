# backend/seed.py
import logging
from app.db.session import SessionLocal
from app.services.user_service import user as user_service
from app.services.patient_service import patient as patient_service
from app.services.note_service import note as note_service
from app.schemas.user import UserCreate
from app.schemas.patient import PatientCreate
from app.schemas.note import NoteCreate
from app.models.patient import Patient
from app.models.note import Note  # Required for delete logic
from app.models.user import User  # Required for delete logic
from datetime import date
import random
from faker import Faker  # Required for realistic demo data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
fake = Faker()

# --- Realistic Demo Data Generation ---
note_templates = [
    "Patient presented with complaints of {complaint}. Vital signs stable. "
    "Plan: {plan}.",
    "Follow-up visit for {condition}. Patient reports {progress}. "
    "Medication adjusted: {med_change}.",
    "Annual physical exam. Patient is a {age}-year-old {gender}. "
    "Reviewed {review_item}. All systems normal.",
    "Consultation regarding {reason}. Discussed options: {options}. "
    "Patient to consider.",
    "Post-operative check-up. Incision healing well. {instructions}.",
    "Patient called requesting prescription refill for {medication}. " "Approved.",
    "ER visit for {reason}. Discharged with instructions for {follow_up}.",
    "Routine prenatal visit. Gestational age {gest_age} weeks. "
    "Fetal heart tones normal.",
    "Well-child check for {age}-month-old. Developmentally appropriate. "
    "Vaccinations given: {vaccines}.",
    "Patient reports {symptom}. Differential diagnosis includes {diff_dx}. "
    "Ordered {tests}.",
]
complaints = [
    "headache",
    "cough",
    "fatigue",
    "shortness of breath",
    "chest pain",
    fake.bs(),
    fake.catch_phrase(),
]
plans = [
    "monitor symptoms",
    "start antibiotics",
    "refer to specialist",
    "order imaging",
    "follow up in 1 week",
]
conditions = [
    "hypertension",
    "diabetes",
    "asthma",
    "arthritis",
    "depression",
    fake.bs(),
]
progress = ["improvement", "no change", "worsening symptoms"]
med_changes = ["increase dosage", "decrease dosage", "switch medication", "no change"]
review_items = ["labs", "medications", "family history", "lifestyle"]
reasons = ["elective surgery", "second opinion", "symptom management", fake.bs()]
options = ["conservative treatment", "physical therapy", "surgical intervention"]
instructions = [
    "Keep wound clean and dry",
    "Continue current medications",
    "Follow up as needed",
]
medications = [
    "Lisinopril",
    "Metformin",
    "Albuterol",
    "Ibuprofen",
    "Sertraline",
    fake.word().capitalize(),
]
follow_ups = ["PCP in 3 days", "Cardiology next week", "Neurology consult"]
symptoms = ["dizziness", "nausea", "joint pain", "rash", "anxiety", fake.bs()]
diff_dx = [
    "viral infection",
    "allergic reaction",
    "musculoskeletal strain",
    "anxiety disorder",
]
tests = ["CBC", "CMP", "Chest X-ray", "ECG", "MRI"]
vaccines = ["DTaP", "Hib", "PCV13", "MMR"]


def generate_random_note(age, gender):
    template = random.choice(note_templates)
    replacements = {
        "{complaint}": random.choice(complaints),
        "{plan}": random.choice(plans),
        "{condition}": random.choice(conditions),
        "{progress}": random.choice(progress),
        "{med_change}": random.choice(med_changes),
        "{age}": str(age),
        "{gender}": gender,
        "{review_item}": random.choice(review_items),
        "{reason}": random.choice(reasons),
        "{options}": random.choice(options),
        "{instructions}": random.choice(instructions),
        "{medication}": random.choice(medications),
        "{follow_up}": random.choice(follow_ups),
        "{gest_age}": str(random.randint(8, 40)),
        "{symptom}": random.choice(symptoms),
        "{diff_dx}": random.choice(diff_dx),
        "{tests}": random.choice(tests),
        "{vaccines}": random.choice(vaccines),
    }
    note_content = template
    for key, value in replacements.items():
        note_content = note_content.replace(key, value)
    note_content += "\n\n" + fake.paragraph(nb_sentences=random.randint(1, 3))
    return note_content


# --- End Demo Data ---


def seed_data():
    db = SessionLocal()
    created_summary = {"users": 0, "patients": 0, "notes": 0}
    deleted_summary = {"users": 0, "patients": 0, "notes": 0}

    try:
        # --- 1. DELETE EXISTING DATA (Runs quickly) ---
        logger.info("Deleting existing data...")
        deleted_notes = db.query(Note).delete()
        deleted_summary["notes"] = deleted_notes
        deleted_patients = db.query(Patient).delete()
        deleted_summary["patients"] = deleted_patients
        deleted_users = db.query(User).delete()
        deleted_summary["users"] = deleted_users
        db.commit()  # Commit deletions immediately
        logger.info(
            f"Finished deleting data. Deleted {deleted_notes} notes, "
            f"{deleted_patients} patients, {deleted_users} users."
        )
        # --- END DELETE ---

        # --- 2. Create Users ---
        test_user_email = "test@example.com"
        test_user_in = UserCreate(email=test_user_email, password="password123")
        test_user = user_service.create(db, obj_in=test_user_in)
        logger.info(f"Test user '{test_user.email}' created.")
        created_summary["users"] += 1

        user_email = fake.email()
        user_in = UserCreate(email=user_email, password="password123")
        user = user_service.create(db, obj_in=user_in)
        logger.info(f"User '{user.email}' created.")
        created_summary["users"] += 1

        # --- 3. Create Patients and Notes (ASYNCHRONOUSLY) ---
        num_patients_to_create = 10
        num_notes_per_patient_min = 2
        num_notes_per_patient_max = 10

        logger.info(f"Attempting to create {num_patients_to_create} new patients...")
        for i in range(num_patients_to_create):
            # --- Patient Creation ---
            gender_choice = random.choice(["male", "female"])
            first_name = (
                fake.first_name_male()
                if gender_choice == "male"
                else fake.first_name_female()
            )
            last_name = fake.last_name()
            birth_date_obj = fake.date_of_birth(minimum_age=1, maximum_age=90)
            age = (date.today() - birth_date_obj).days // 365

            patient_in = PatientCreate(
                name=[{"family": last_name, "given": [first_name]}],
                gender=gender_choice,
                birthDate=birth_date_obj,
            )

            # Create patient using the service (handles commit)
            patient: Patient = patient_service.create(db, obj_in=patient_in)
            logger.info(
                f"Patient '{first_name} {last_name}' with ID {patient.id} created."
            )
            created_summary["patients"] += 1

            # --- Note Creation (Triggers Celery Task) ---
            if patient.id is not None:
                patient_id = int(patient.id)  # type: ignore
                num_notes = random.randint(
                    num_notes_per_patient_min, num_notes_per_patient_max
                )

                for _ in range(num_notes):
                    note_content = generate_random_note(age, gender_choice)
                    note_in = NoteCreate(
                        content=note_content,
                        patient_id=patient_id,
                    )

                    # It returns immediately without waiting for the AI task to finish.
                    note = note_service.create(db, obj_in=note_in)

                    logger.info(
                        f"Note with ID {note.id} created for patient {patient.id}. "
                        f"(AI Task Dispatched)"
                    )
                    created_summary["notes"] += 1

            else:
                logger.warning(
                    f"Patient '{first_name} {last_name}' created but ID is None, "
                    f"cannot add notes."
                )

        logger.info("Database seeding finished.")
        # --- 4. Return Summary (Quickly) ---
        return {"deleted": deleted_summary, "created": created_summary}

    except Exception as e:
        logger.error(f"An error occurred during seeding: {e}", exc_info=True)
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()


if __name__ == "__main__":
    result = seed_data()
    print(f"Seeding result: {result}")
