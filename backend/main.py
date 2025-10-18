# path: backend/main.py

from fastapi import FastAPI
from app.api.v1 import users, auth, patients, notes

app = FastAPI(title="Health AI Boilerplate API")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the Health AI Boilerplate API"}


@app.get("/debug-config")
def debug_config():
    from app.core.config import settings

    return {"database_url": settings.DATABASE_URL}


# Include the routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["patients"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])
