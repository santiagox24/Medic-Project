from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CopilotConversationCreate(BaseModel):
    patient_id: int
    title: str | None = Field(default=None, max_length=160)


class CopilotConversationRead(BaseModel):
    id: str
    patient_id: int
    title: str | None = None
    model: str
    summary: str = ""
    archived: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CopilotMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class CopilotSource(BaseModel):
    type: str
    id: int | str
    label: str


class CopilotMessageRead(BaseModel):
    id: int
    role: str
    content: str
    sources: list[CopilotSource] = Field(default_factory=list)
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CopilotConversationDetail(CopilotConversationRead):
    messages: list[CopilotMessageRead] = Field(default_factory=list)


class CopilotReply(BaseModel):
    conversation_id: str
    message: CopilotMessageRead
