from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    document_id: str
    username: str
    name: str
    email: str
    tel: str
    age: int
    gender: str
    adress: str
    city: str
    country: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str