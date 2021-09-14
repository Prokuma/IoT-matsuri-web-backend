from pydantic import BaseModel, validator, EmailStr
from datetime import date, datetime
from typing import Optional

class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserSignInRequest(BaseModel):
    email: EmailStr
    password: str

class UserWithToken(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    token: str

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

class UserStatus(BaseModel):
    status: str