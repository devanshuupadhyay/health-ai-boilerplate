# path: backend/main.py

# Imports
from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.logging_config import configure_logging, get_logger
from app.api.v1 import users, auth, patients, notes
from app.api import deps
import seed

# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# --- ADD SENTRY IMPORTS ---
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from app.core.config import settings  # Need settings for DSN
from prometheus_fastapi_instrumentator import Instrumentator

# --- INITIALIZE SENTRY SDK ---
if settings.SENTRY_DSN:
    try:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            # Add integrations for frameworks/libraries you use
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration(),
                CeleryIntegration(),
            ],
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # Adjust sampling in production.
            traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions. Adjust sampling in production.
            profiles_sample_rate=1.0,
            # You can add environment, release version etc. here too
            # environment="development", # Example
        )
        print(
            "Sentry SDK initialized successfully."
        )  # Use print here as logger might not be ready yet
    except Exception as e:
        print(f"Failed to initialize Sentry SDK: {e}")  # Use print for early errors
else:
    print("SENTRY_DSN not found, skipping Sentry initialization.")
# --- END SENTRY SETUP ---

# Configure logging & OTEL (already done in previous step)
configure_logging()

log = get_logger(__name__)
app = FastAPI(title="Health AI Boilerplate API")

# This automatically adds tracing to incoming requests
# FastAPIInstrumentor().instrument_app(app)
# log.info("FastAPI application instrumented with OpenTelemetry.")

# Exposes /metrics endpoint
Instrumentator().instrument(app).expose(app)
log.info("FastAPI application instrumented with Prometheus.")

log.info("Starting Health AI Boilerplate API...")  # Keep this log


# --- Root endpoint ---
@app.get("/")
def read_root():
    log.info("Root endpoint called")
    return {"status": "ok", "message": "Welcome to the Health AI Boilerplate API"}


# --- Debug config endpoint ---
@app.get("/debug-config")
def debug_config():
    from app.core.config import settings

    log.info("Debug config endpoint called")
    return {"database_url": settings.DATABASE_URL}


@app.post("/api/v1/debug/seed-data", status_code=status.HTTP_200_OK, tags=["debug"])
def run_seed_data(
    db: Session = Depends(deps.get_db),
):  # db dependency is kept for consistency but not directly used by seed_data()
    """
    Executes the database seeding script with more comprehensive data.
    **Warning:** Modifies the database. Intended for development/demo.
    Returns a summary of created items.
    """
    log.info("Seed data endpoint called.")
    try:
        # seed.seed_data manages its own session
        summary = seed.seed_data()
        if "error" in summary:
            raise HTTPException(
                status_code=500, detail=f"Seeding failed: {summary['error']}"
            )
        log.info(f"Seeding completed successfully: {summary}")
        return {"status": "success", "summary": summary}
    except Exception as e:
        log.error(f"Error executing seed data endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Internal server error during seeding: {str(e)}"
        )


# --- Include routers ---
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["patients"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])

log.info("API routers included.")
