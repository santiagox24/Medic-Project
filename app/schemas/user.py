from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from typing import Optional


class UserBase(BaseModel):
    document_id: str
    username: str
    name: str
    email: EmailStr
    tel: str
    age: int
    gender: str
    address: str
    city: str
    country: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str