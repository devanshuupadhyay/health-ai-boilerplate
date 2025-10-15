# path: backend/app/api/v1/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import services, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.user.User)
def create_new_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
):
    """
    Create new user.
    """
    user = services.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = services.user.create(db, obj_in=user_in)
    return user