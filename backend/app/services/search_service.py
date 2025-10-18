# backend/app/services/search_service.py
import meilisearch

# import logging # Keep commented out if using Structlog now
from app.core.config import settings
from app.models.note import Note
from app.core.logging_config import get_logger

# --- ADD THESE IMPORTS ---
from typing import Dict, Any

# --- END IMPORTS ---


log = get_logger(__name__)

# ... (client initialization code) ...
try:
    client = meilisearch.Client(settings.MEILI_URL, settings.MEILI_MASTER_KEY)
    notes_index = client.index("notes")
    log.info("Meilisearch client initialized", meili_url=settings.MEILI_URL)
except Exception as e:
    log.error("Failed to initialize Meilisearch client", error=str(e), exc_info=True)
    client = None


def add_note_to_index(note: Note):
    """Adds or updates a note document in the Meilisearch 'notes' index."""
    if not client:
        log.error(
            "Meilisearch client not available, skipping indexing",
            note_id=note.id if note else None,
        )
        return False

    if not note or note.id is None:
        log.error("Invalid note object or note ID missing for indexing.")
        return False

    try:
        # --- ADD TYPE HINT HERE ---
        document: Dict[str, Any] = {
            "id": note.id,
            "patient_id": note.patient_id,
            "content": note.content,
            # Ensure summary is included, even if None, for consistent schema
            "summary": note.summary if note.summary is not None else "",
        }
        # --- END TYPE HINT ---

        notes_index = client.index("notes")
        # Ensure we are passing a LIST containing the document dictionary
        task = notes_index.add_documents([document], primary_key="id")
        log.info(
            "Task submitted to Meilisearch",
            note_id=note.id,
            task_uid=task.task_uid,
        )
        return True
    except Exception as e:
        log.error(
            "Failed to add/update note in Meilisearch",
            note_id=note.id,
            error=str(e),
            exc_info=True,
        )
        return False
