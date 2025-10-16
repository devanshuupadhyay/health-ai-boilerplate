# backend/app/services/user_service.py
from typing import Optional, Any, Type
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, model: Type[User]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[User]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = UserService(User)
