from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    access_token: str
    refresh_token:str
    created_at: datetime

class UserResponse(UserBase):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int | None = None

    class Config:
        from_attributes = True