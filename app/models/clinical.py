from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clinician_id: Mapped[str] = mapped_column(ForeignKey("users.document_id"), index=True)
    document: Mapped[str] = mapped_column(String(64), index=True)
    full_name: Mapped[str] = mapped_column(String(160), index=True)
    document_type: Mapped[str | None] = mapped_column(String(16), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    second_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    first_surname: Mapped[str | None] = mapped_column(String(80), nullable=True)
    second_surname: Mapped[str | None] = mapped_column(String(80), nullable=True)
    birth_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sex: Mapped[str | None] = mapped_column(String(32), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(64), nullable=True)
    blood_type: Mapped[str | None] = mapped_column(String(8), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(48), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str | None] = mapped_column(String(32), nullable=True, default="Activo")
    site: Mapped[str | None] = mapped_column(String(128), nullable=True)
    city: Mapped[str | None] = mapped_column(String(128), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    regime: Mapped[str | None] = mapped_column(String(64), nullable=True)
    administrator: Mapped[str | None] = mapped_column(String(160), nullable=True)
    marital_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    ethnic_group: Mapped[str | None] = mapped_column(String(128), nullable=True)
    population_group: Mapped[str | None] = mapped_column(String(128), nullable=True)
    occupation: Mapped[str | None] = mapped_column(String(128), nullable=True)
    education_level: Mapped[str | None] = mapped_column(String(128), nullable=True)
    zone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    stratum: Mapped[str | None] = mapped_column(String(16), nullable=True)
    religion: Mapped[str | None] = mapped_column(String(128), nullable=True)
    allergies: Mapped[list] = mapped_column(JSON, default=list)
    conditions: Mapped[list] = mapped_column(JSON, default=list)
    medications: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clinician_id: Mapped[str] = mapped_column(ForeignKey("users.document_id"), index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), index=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    reason: Mapped[str] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(String(32), default="Pendiente")


class ClinicalSession(Base):
    __tablename__ = "clinical_sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    clinician_id: Mapped[str] = mapped_column(ForeignKey("users.document_id"), index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    reason: Mapped[str] = mapped_column(String(300))
    soap_notes: Mapped[str] = mapped_column(Text)
    diagnosis: Mapped[str | None] = mapped_column(String(300), nullable=True)
    diagnosis_code: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    diagnosis_uri: Mapped[str | None] = mapped_column(String(512), nullable=True)
    diagnosis_release: Mapped[str | None] = mapped_column(String(32), nullable=True)
    plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    vitals: Mapped[dict] = mapped_column(JSON, default=dict)
    medications: Mapped[list] = mapped_column(JSON, default=list)
