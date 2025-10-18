# backend/app/tasks/process_note.py
import requests
from celery_worker import celery
from app.db.session import SessionLocal
from app.services.note_service import note as note_service

AI_SERVICE_URL = "http://ai:8001/summarize"


@celery.task
def summarize_note_task(note_id: int):
    """
    Celery task to generate and save a summary for a clinical note.
    """
    db = SessionLocal()
    try:
        note = note_service.get(db, id=note_id)
        if not note:
            print(f"Note with ID {note_id} not found.")
            return

        # Call the AI microservice
        response = requests.post(AI_SERVICE_URL, json={"text": note.content})
        response.raise_for_status()  # Raise an exception for bad status codes

        summary = response.json().get("summary")

        # For now, we'll just print the summary.
        # In a future step, we would save this to the database.
        print(f"Summary for Note ID {note_id}: {summary}")

    except requests.exceptions.RequestException as e:
        print(f"Error calling AI service for Note ID {note_id}: {e}")
    finally:
        db.close()

    return summary
