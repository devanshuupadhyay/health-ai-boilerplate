# backend/app/models/__init__.py
from .user import User
from .patient import Patient
from .note import Note

# This tells Python and linters that these are the public exports of this package
__all__ = ["User", "Patient", "Note"]
