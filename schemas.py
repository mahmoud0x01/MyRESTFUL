from typing import Union

from pydantic import BaseModel

class login(BaseModel):
    id: str
    password: str

class postBase(BaseModel):
    title: str
    description: str


class post(postBase):

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    posts: list[post] = []
    class Config:
        orm_mode = True

class LikeCreate(BaseModel):
    liker_id: str
    post_id: str