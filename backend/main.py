# path: backend/main.py

from app.core.logging_config import configure_logging, get_logger
from fastapi import FastAPI
from app.api.v1 import users, auth, patients, notes

# Configure logging at the start of the application
configure_logging()

# Initialize logger
log = get_logger(__name__)


app = FastAPI(title="Health AI Boilerplate API")

log.info("Starting Health AI Boilerplate API...")


@app.get("/")
def read_root():
    log.info("Root endpoint called")
    return {"status": "ok", "message": "Welcome to the Health AI Boilerplate API"}


@app.get("/debug-config")
def debug_config():
    from app.core.config import settings

    log.info("Debug config endpoint called")
    return {"database_url": settings.DATABASE_URL}


# Include the routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["patients"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])

log.info("API routers included.")
