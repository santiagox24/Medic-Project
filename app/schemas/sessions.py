from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
