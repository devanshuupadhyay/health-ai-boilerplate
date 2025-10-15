# path: backend/app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.user_service import user as user_service
from app.schemas.user import User, UserCreate
from app.api import deps

router = APIRouter()


@router.post("/", response_model=User)
def create_new_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
):
    """
    Create new user.
    """
    user = user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = user_service.create(db, obj_in=user_in)
    return user
