from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.clinical import Appointment, ClinicalSession, Patient
from models.user import User
from schemas.clinical import AppointmentCreate, AppointmentRead, ClinicalSessionCreate, ClinicalSessionRead, PatientCreate, PatientRead
from routes.user import get_current_user_profile

router = APIRouter(prefix="/clinical", tags=["clinical"])

async def clinician(token_user=Depends(get_current_user_profile)):
    return token_user["document_id"]

async def owned_patient(patient_id: int, clinician_id: str, db: AsyncSession) -> Patient:
    patient = (await db.execute(select(Patient).where(Patient.id == patient_id, Patient.clinician_id == clinician_id))).scalar_one_or_none()
    if not patient: raise HTTPException(404, "Paciente no encontrado")
    return patient

@router.get("/patients", response_model=list[PatientRead])
async def patients(q: str | None = None, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    stmt = select(Patient).where(Patient.clinician_id == clinician_id).order_by(Patient.full_name)
    if q: stmt = stmt.where(Patient.full_name.ilike(f"%{q}%"))
    return (await db.execute(stmt)).scalars().all()

@router.post("/patients", response_model=PatientRead, status_code=201)
async def create_patient(data: PatientCreate, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    item = Patient(**data.model_dump(), clinician_id=clinician_id); db.add(item); await db.commit(); await db.refresh(item); return item

@router.get("/patients/{patient_id}", response_model=PatientRead)
async def patient(patient_id: int, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    return await owned_patient(patient_id, clinician_id, db)

@router.get("/patients/{patient_id}/sessions", response_model=list[ClinicalSessionRead])
async def patient_sessions(patient_id: int, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    await owned_patient(patient_id, clinician_id, db)
    return (await db.execute(select(ClinicalSession).where(ClinicalSession.patient_id == patient_id, ClinicalSession.clinician_id == clinician_id).order_by(ClinicalSession.created_at.desc()))).scalars().all()

@router.post("/sessions", response_model=ClinicalSessionRead, status_code=201)
async def create_session(data: ClinicalSessionCreate, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    await owned_patient(data.patient_id, clinician_id, db)
    item = ClinicalSession(**data.model_dump(), clinician_id=clinician_id); db.add(item); await db.commit(); await db.refresh(item); return item

@router.get("/appointments", response_model=list[AppointmentRead])
async def appointments(clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(Appointment).where(Appointment.clinician_id == clinician_id).order_by(Appointment.scheduled_at))).scalars().all()

@router.post("/appointments", response_model=AppointmentRead, status_code=201)
async def create_appointment(data: AppointmentCreate, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    await owned_patient(data.patient_id, clinician_id, db)
    item = Appointment(**data.model_dump(), clinician_id=clinician_id); db.add(item); await db.commit(); await db.refresh(item); return item

@router.get("/dashboard")
async def dashboard(clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    patients_count = (await db.execute(select(func.count(Patient.id)).where(Patient.clinician_id == clinician_id))).scalar_one()
    today = datetime.now(timezone.utc).date()
    appointments_count = (await db.execute(select(func.count(Appointment.id)).where(Appointment.clinician_id == clinician_id, func.date(Appointment.scheduled_at) == today))).scalar_one()
    return {"patients": patients_count, "appointments_today": appointments_count, "alerts": 0, "adherence": None}

@router.post("/copilot/{patient_id}")
async def copilot(patient_id: int, payload: dict, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    patient = await owned_patient(patient_id, clinician_id, db); question = str(payload.get("question", ""))
    recent = (await db.execute(select(ClinicalSession).where(ClinicalSession.patient_id == patient.id).order_by(ClinicalSession.created_at.desc()).limit(3))).scalars().all()
    meds = ", ".join(m.get("name", m.get("nombre", "medicamento")) for m in patient.medications) or "sin medicamentos registrados"
    answer = f"Contexto de {patient.full_name}: antecedentes: {', '.join(patient.conditions) or 'sin antecedentes registrados'}; alergias: {', '.join(patient.allergies) or 'ninguna registrada'}; tratamiento: {meds}. "
    if recent: answer += f"La última sesión fue por {recent[0].reason}. "
    answer += "Este copiloto organiza la información del expediente y requiere validación clínica profesional; no sustituye el juicio médico."
    return {"answer": answer, "question": question}
