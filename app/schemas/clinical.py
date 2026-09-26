from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

class PatientFields(BaseModel):
    document_type: str | None = Field(default="CC", max_length=16)
    document: str
    full_name: str | None = Field(default=None, max_length=160)
    first_name: str | None = Field(default=None, max_length=80)
    second_name: str | None = Field(default=None, max_length=80)
    first_surname: str | None = Field(default=None, max_length=80)
    second_surname: str | None = Field(default=None, max_length=80)
    birth_date: datetime | None = None
    sex: str | None = Field(default=None, max_length=32)
    gender: str | None = Field(default=None, max_length=64)
    blood_type: str | None = Field(default=None, max_length=8)
    phone: str | None = Field(default=None, max_length=48)
    email: EmailStr | None = None
    status: str | None = Field(default="Activo", max_length=32)
    site: str | None = Field(default=None, max_length=128)
    city: str | None = Field(default=None, max_length=128)
    address: str | None = Field(default=None, max_length=255)
    regime: str | None = Field(default=None, max_length=64)
    administrator: str | None = Field(default=None, max_length=160)
    marital_status: str | None = Field(default=None, max_length=64)
    ethnic_group: str | None = Field(default=None, max_length=128)
    population_group: str | None = Field(default=None, max_length=128)
    occupation: str | None = Field(default=None, max_length=128)
    education_level: str | None = Field(default=None, max_length=128)
    zone: str | None = Field(default=None, max_length=32)
    stratum: str | None = Field(default=None, max_length=16)
    religion: str | None = Field(default=None, max_length=128)
    allergies: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)
    medications: list[dict] = Field(default_factory=list)

class PatientCreate(PatientFields):
    @model_validator(mode="after")
    def build_full_name(self):
        if not self.full_name:
            parts = [self.first_name, self.second_name, self.first_surname, self.second_surname]
            self.full_name = " ".join(part.strip() for part in parts if part and part.strip())
        if not self.full_name:
            raise ValueError("Ingrese al menos un nombre o el nombre completo del paciente")
        return self

class PatientRead(PatientFields):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PatientUpdate(BaseModel):
    document_type: str | None = Field(default=None, max_length=16)
    document: str | None = None
    full_name: str | None = Field(default=None, max_length=160)
    first_name: str | None = Field(default=None, max_length=80)
    second_name: str | None = Field(default=None, max_length=80)
    first_surname: str | None = Field(default=None, max_length=80)
    second_surname: str | None = Field(default=None, max_length=80)
    birth_date: datetime | None = None
    sex: str | None = Field(default=None, max_length=32)
    gender: str | None = Field(default=None, max_length=64)
    blood_type: str | None = Field(default=None, max_length=8)
    phone: str | None = Field(default=None, max_length=48)
    email: EmailStr | None = None
    status: str | None = Field(default=None, max_length=32)
    site: str | None = Field(default=None, max_length=128)
    city: str | None = Field(default=None, max_length=128)
    address: str | None = Field(default=None, max_length=255)
    regime: str | None = Field(default=None, max_length=64)
    administrator: str | None = Field(default=None, max_length=160)
    marital_status: str | None = Field(default=None, max_length=64)
    ethnic_group: str | None = Field(default=None, max_length=128)
    population_group: str | None = Field(default=None, max_length=128)
    occupation: str | None = Field(default=None, max_length=128)
    education_level: str | None = Field(default=None, max_length=128)
    zone: str | None = Field(default=None, max_length=32)
    stratum: str | None = Field(default=None, max_length=16)
    religion: str | None = Field(default=None, max_length=128)
    allergies: list[str] | None = None
    conditions: list[str] | None = None
    medications: list[dict] | None = None

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
    diagnosis_code: str | None = Field(default=None, max_length=32)
    diagnosis_uri: str | None = Field(default=None, max_length=512)
    diagnosis_release: str | None = Field(default=None, max_length=32)
    plan: str | None = None
    vitals: dict = Field(default_factory=dict)
    medications: list[dict] = Field(default_factory=list)

class ClinicalSessionRead(ClinicalSessionCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ICD11SearchResult(BaseModel):
    code: str
    title: str
    uri: str
    release: str
