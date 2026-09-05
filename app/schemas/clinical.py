from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class PatientCreate(BaseModel):
    document: str
    full_name: str
    birth_date: datetime | None = None
    sex: str | None = None
    blood_type: str | None = None
    phone: str | None = None
    allergies: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)
    medications: list[dict] = Field(default_factory=list)

class PatientRead(PatientCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class AppointmentCreate(BaseModel):
    patient_id: int
    scheduled_at: datetime
    reason: str = Field(min_length=3, max_length=300)
    status: Literal["Pendiente", "Confirmada", "Completada", "Cancelada"] = "Pendiente"

class AppointmentUpdate(BaseModel):
    patient_id: int | None = None
    scheduled_at: datetime | None = None
    reason: str | None = Field(default=None, min_length=3, max_length=300)
    status: Literal["Pendiente", "Confirmada", "Completada", "Cancelada"] | None = None

class AppointmentRead(AppointmentCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ClinicalSessionCreate(BaseModel):
    patient_id: int
    reason: str
    soap_notes: str
    diagnosis: str | None = None
    plan: str | None = None
    vitals: dict = Field(default_factory=dict)
    medications: list[dict] = Field(default_factory=list)

class ClinicalSessionRead(ClinicalSessionCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
