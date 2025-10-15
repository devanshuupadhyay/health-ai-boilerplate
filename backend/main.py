# path: backend/main.py

from fastapi import FastAPI
from app.api.v1 import users  # Import the users router
from app.core.config import settings

app = FastAPI(title="Health AI Boilerplate API")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the Health AI Boilerplate API"}


# Include the router
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/debug-config")
def debug_config():
    return {"database_url": settings.DATABASE_URL}
