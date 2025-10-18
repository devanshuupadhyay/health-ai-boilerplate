# backend/app/services/search_service.py
import meilisearch
import logging
from app.core.config import settings
from app.models.note import Note  # Import the Note model

logger = logging.getLogger(__name__)

# Initialize Meilisearch client
try:
    client = meilisearch.Client(settings.MEILI_URL, settings.MEILI_MASTER_KEY)
    # Try to get the index, create if it doesn't exist (basic health check)
    notes_index = client.index("notes")
    # Optional: Configure index settings if needed (e.g., searchable attributes)
    # notes_index.update_settings({
    #     'searchableAttributes': ['content', 'summary'],
    #     'filterableAttributes': ['patient_id'],
    # })
    logger.info("Meilisearch client initialized and 'notes' index ensured.")
except Exception as e:
    logger.error(f"Failed to initialize Meilisearch client: {e}")
    # Depending on your error handling strategy, you might want to
    # raise the exception or handle it differently.
    # For now, we log the error and might have issues later.
    client = None  # Indicate client failed to initialize


def add_note_to_index(note: Note):
    """Adds or updates a note document in the Meilisearch 'notes' index."""
    if not client:
        logger.error("Meilisearch client not available. Skipping indexing.")
        return False

    if not note or note.id is None:
        logger.error("Invalid note object passed to add_note_to_index.")
        return False

    try:
        # Prepare the document for Meilisearch
        # We only index fields relevant for searching
        document = {
            "id": note.id,  # Meilisearch requires a unique 'id' field
            "patient_id": note.patient_id,
            "content": note.content,
            "summary": note.summary,
        }
        notes_index = client.index("notes")
        task = notes_index.add_documents([document], primary_key="id")
        logger.info(
            f"Task submitted to Meilisearch for adding/updating Note ID {note.id}. "
            f"Task UID: {task.task_uid}"
        )
        # Note: Meilisearch indexing is asynchronous. We don't wait for completion here.
        return True
    except Exception as e:
        logger.error(f"Failed to add/update Note ID {note.id} in Meilisearch: {e}")
        return False
