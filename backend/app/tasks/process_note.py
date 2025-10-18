# backend/app/tasks/process_note.py
import requests
from celery_worker import celery
from app.db.session import SessionLocal
from app.services.note_service import note as note_service  # Keep this

# Remove the unused patient_service import if it exists

AI_SERVICE_URL = "http://ai:8001/summarize"


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
            print(f"Note with ID {note_id} not found.")
            # Use return instead of continuing in a finally block
            db.close()
            return None  # Return None or some indicator of failure

        # Call the AI microservice
        response = requests.post(AI_SERVICE_URL, json={"text": note.content})
        response.raise_for_status()  # Raise an exception for bad status codes

        summary_json = response.json()
        summary = summary_json.get("summary")

        # --- ADD THESE LINES TO SAVE THE SUMMARY ---
        if summary:
            note.summary = summary
            db.add(note)  # Add the updated note object to the session
            db.commit()  # Commit the changes
            db.refresh(note)  # Refresh to get the updated state if needed
            print(f"Summary saved for Note ID {note_id}: {summary}")
        else:
            print(f"No summary generated for Note ID {note_id}.")
        # --- END OF ADDED LINES ---

    except requests.exceptions.RequestException as e:
        print(f"Error calling AI service for Note ID {note_id}: {e}")
        # Optionally rollback changes if the AI call fails
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred for Note ID {note_id}: {e}")
        db.rollback()  # Rollback on any other error during processing
    finally:
        db.close()

    return summary  # Return the summary (or None if failed)
