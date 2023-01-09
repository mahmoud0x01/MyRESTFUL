from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError
from schemas import TokenPayload, loggedinuser
from sqlalchemy.orm import Session

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


 def get_current_user(token: str = Depends(reuseable_oauth)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user