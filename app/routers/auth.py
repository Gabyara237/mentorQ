

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token
from app.services.auth_service import AuthService
from app.utils.dependencies import get_current_user
from app.utils.security import create_access_token


router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup_user(user_data: UserCreate, session:Annotated[Session,Depends(get_session)]):
    
    return AuthService.create_user(session, user_data)


@router.post("/signin", response_model=Token)
def signin_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session:Annotated[Session, Depends(get_session)]):

    user = AuthService.authenticate_user(session,form_data.username,form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail= "Incorrect username or password",headers={"WWW-Authenticate":"Bearer"})
    
    expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(data ={ "sub": str(user.id)}, expires_delta= expires_delta)

    return Token(access_token=access_token,token_type="bearer")


@router.get("/me", response_model= UserResponse)
def get_me(current_user: Annotated[User,Depends(get_current_user)]):
    return current_user
