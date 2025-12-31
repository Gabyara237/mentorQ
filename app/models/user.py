
from enum import Enum
from sqlmodel import VARCHAR, Column, SQLModel, Field

class UserRole(str, Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    

class User(SQLModel, table =True):
    __tablename__ = "users"

    id: int | None = Field(default = None, primary_key =True)
    username: str = Field(sa_column = Column("username",VARCHAR(50), unique=True,index= True)) 
    email: str = Field(sa_column = Column("email", VARCHAR(100), unique=True, index =True))
    password: str 
    role: UserRole
    bio: str | None = Field(default=None)
    avatar: str | None = Field(default=None)
    is_available: bool = Field(default=True)
