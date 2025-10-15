# path: backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr

# Shared properties that all user-related schemas will have.
class UserBase(BaseModel):
    email: EmailStr


# Properties required when creating a new user via the API.
class UserCreate(UserBase):
    password: str


# Properties to return to the client.
# This schema will be used when reading user data.
class User(UserBase):
    id: int
    is_active: bool

    # This Config class tells Pydantic to map to SQLAlchemy ORM models.
    class Config:
        from_attributes = True