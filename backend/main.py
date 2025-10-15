# path: backend/main.py

from fastapi import FastAPI
from app.api.v1 import users  # Import the users router

app = FastAPI(title="Health AI Boilerplate API")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the Health AI Boilerplate API"}


# Include the router
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
