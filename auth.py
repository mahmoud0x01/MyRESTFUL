import os
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Union, Any
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import schemas

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "JWT_SECRET_KEY"   # should be kept secret
JWT_REFRESH_SECRET_KEY = "JWT_REFRESH_SECRET_KEY"   # should be kept secret


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt



def authorize_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = None
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if (username is None):
            return credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        return credentials_exception
    return username