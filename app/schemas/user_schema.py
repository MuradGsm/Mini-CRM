from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserDB(UserUpdate):
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    create_at: datetime
    update_at: datetime

    class Config:
        orm_mode=True
