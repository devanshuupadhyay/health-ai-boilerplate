# backend/app/tasks/process_note.py
import requests
import logging
from celery_worker import celery
from app.db.session import SessionLocal
from app.services.note_service import note as note_service
from app.services.search_service import add_note_to_index

# Remove the unused patient_service import if it exists

AI_SERVICE_URL = "http://ai:8001/summarize"
logger = logging.getLogger(__name__)


@celery.task
def summarize_note_task(note_id: int):
    """
    Celery task to generate and save a summary for a clinical note.
    """
    db = SessionLocal()
    summary = None  # Initialize summary variable
    try:
        note = note_service.get(db, id=note_id)
        if not note:
            logger.warning(f"Note with ID {note_id} not found.")
            # Use return instead of continuing in a finally block
            db.close()
            return None  # Return None or some indicator of failure

        # Call the AI microservice
        response = requests.post(AI_SERVICE_URL, json={"text": note.content})
        response.raise_for_status()  # Raise an exception for bad status codes

        summary_json = response.json()
        summary = summary_json.get("summary")

        if summary:
            note.summary = summary
            db.add(note)  # Add the updated note object to the session
            db.commit()  # Commit the changes
            db.refresh(note)  # Refresh to get the updated state if needed
            logger.info(f"Summary saved for Note ID {note_id}: {summary}")
            add_note_to_index(note)
        else:
            logger.warning(f"No summary generated for Note ID {note_id}.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling AI service for Note ID {note_id}: {e}")
        # Optionally rollback changes if the AI call fails
        db.rollback()
    except Exception as e:
        logger.error(f"An unexpected error occurred for Note ID {note_id}: {e}")
        db.rollback()  # Rollback on any other error during processing
    finally:
        db.close()

    return summary  # Return the summary (or None if failed)
