
from datetime import timedelta, timezone, datetime
from app.config import SECRET_KEY, ALGORITHM
import jwt
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None =None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc)+ expires_delta
    else:
        expire = datetime.now(timezone.utc)+ timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm = ALGORITHM)
    
    return encoded_jwt

def decode_token(token):
    return jwt.decode(token,SECRET_KEY,algorithms =[ALGORITHM])
       