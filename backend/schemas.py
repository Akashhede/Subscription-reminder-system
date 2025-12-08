
from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    phone: Optional[str] = None
    email_alerts_enabled: bool = True
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email_alerts_enabled: Optional[bool] = None
    phone: Optional[str] = None

class SubscriptionCreate(BaseModel):
    name: str
    renewal_date: date
    note: Optional[str] = None

class SubscriptionOut(BaseModel):
    id: int
    name: str
    renewal_date: date
    note: Optional[str] = None
    user_id: int
    class Config:
        from_attributes = True

class TestEmailRequest(BaseModel):
    subject: str
    message: str

class AlertResponse(BaseModel):
    status: str
    message: str
