from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class SessionBase(BaseModel):
    date: datetime
    title: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    analysis: Optional[str] = None


class SessionCreate(SessionBase):
    user_id: str

class SessionUpdate(BaseModel):
    answer: str
    analysis: Optional[str] = None


class SessionRead(SessionBase):
    id: int
    user_id: str

    model_config = ConfigDict(from_attributes=True)
