from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SessionBase(BaseModel):
    date: datetime
    questions: str
    #analysis: str


class SessionCreate(SessionBase):
    user_id: str

class SessionUpdate(BaseModel):
    answer: str


class SessionRead(SessionBase):
    id:int
    user_id:str
    questions: str
    answers: str

    class Config:
        orm_mode=True
