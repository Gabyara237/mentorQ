
from pydantic import BaseModel, EmailStr

from app.models.user import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    bio: str | None
    avatar: str | None
    is_available: bool

