# path: backend/app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# The Engine is the starting point for any SQLAlchemy application.
# It's the central source of connectivity to a particular database.
engine = create_engine(
    settings.DATABASE_URL,
)

# A sessionmaker provides a factory for creating Session objects.
# Each instance of SessionLocal will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We will inherit from this class to create each of the ORM models.
Base = declarative_base()