from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class ClientCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] =None
    notes: Optional[str] =None


class  ClientUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] =None
    notes: Optional[str] =None

class ClientOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str] =None
    notes: Optional[str] =None
    owner_id: int
    create_at: datetime
    update_at: datetime

    model_config = ConfigDict(from_attributes=True)