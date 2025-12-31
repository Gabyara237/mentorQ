
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash, verify_password


class AuthService:
    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:

        normalized_username = user_data.username.strip().lower()
       
        query = select(User).where(User.username == normalized_username)
        user = session.exec(query).first()
        
        if user:
            raise HTTPException(status_code=400,detail="Username already registered")
        
        
        normalized_email = user_data.email.strip().lower()
        query = select(User).where(User.email== normalized_email )
        user = session.exec(query).first()
        
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        password_hash = get_password_hash(user_data.password)

        new_user = User(
            username=normalized_username,
            email= normalized_email,
            password_hash= password_hash,
            role=user_data.role, 
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user
    
    @staticmethod
    def authenticate_user(session: Session, username:str, password:str)-> User | None:
        
        normalized_username = username.strip().lower()
        query = select(User).where(User.username==normalized_username)
        user = session.exec(query).first()

        if not user:
            return None
        
        if not verify_password(password,user.password_hash):
            return None
    
        return user
       
