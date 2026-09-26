from datetime import datetime, timezone
import re
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.clinical import Appointment, ClinicalSession, Patient
from models.user import User
from schemas.clinical import AppointmentCreate, AppointmentRead, AppointmentUpdate, ClinicalSessionCreate, ClinicalSessionRead, ICD11SearchResult, PatientCreate, PatientRead, PatientUpdate
from routes.user import get_current_user_profile
from config import ICD11_API_URL, ICD11_LANGUAGE, ICD11_RELEASE

router = APIRouter(prefix="/clinical", tags=["clinical"])

async def clinician(token_user=Depends(get_current_user_profile)):
    return token_user["document_id"]

async def owned_patient(patient_id: int, clinician_id: str, db: AsyncSession) -> Patient:
    patient = (await db.execute(select(Patient).where(Patient.id == patient_id, Patient.clinician_id == clinician_id))).scalar_one_or_none()
    if not patient: raise HTTPException(404, "Paciente no encontrado")
    return patient

async def owned_appointment(appointment_id: int, clinician_id: str, db: AsyncSession) -> Appointment:
    item = (await db.execute(select(Appointment).where(Appointment.id == appointment_id, Appointment.clinician_id == clinician_id))).scalar_one_or_none()
    if not item: raise HTTPException(404, "Cita no encontrada")
    return item

PATIENT_NAME_FIELDS = ("first_name", "second_name", "first_surname", "second_surname")

def patient_display_name(values: dict, fallback: str = "") -> str:
    """Build the compatible display name from the structured intake fields."""
    name = " ".join(str(values.get(field) or "").strip() for field in PATIENT_NAME_FIELDS).strip()
    return name or str(values.get("full_name") or fallback).strip()

def clean_icd11_title(value: str) -> str:
    """The ICD search response highlights matches with HTML <em> tags."""
    return re.sub(r"<[^>]+>", "", value or "").strip()

@router.get("/icd11/search", response_model=list[ICD11SearchResult])
async def search_icd11(q: str, clinician_id: str = Depends(clinician)):
    query = q.strip()
    if len(query) < 2:
        return []

    url = f"{ICD11_API_URL}/icd/release/11/{ICD11_RELEASE}/mms/search"
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(
                url,
                params={"q": query},
                headers={"API-Version": "v2", "Accept-Language": ICD11_LANGUAGE, "Accept": "application/json"},
            )
            response.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(status_code=503, detail="El servicio ICD-11 no está disponible en este momento")

    try:
        entities = response.json().get("destinationEntities", [])
    except ValueError:
        raise HTTPException(status_code=502, detail="El servicio ICD-11 devolvió una respuesta inválida")

    results = []
    for entity in entities:
        code = entity.get("theCode") or entity.get("code")
        title = clean_icd11_title(entity.get("title", ""))
        uri = entity.get("id") or entity.get("stemId")
        if code and title and uri:
            results.append({"code": code, "title": title, "uri": uri, "release": ICD11_RELEASE})
        if len(results) == 10:
            break
    return results

async def ensure_available(scheduled_at: datetime, clinician_id: str, db: AsyncSession, exclude_id: int | None = None):
    stmt = select(Appointment.id).where(
        Appointment.clinician_id == clinician_id,
        Appointment.scheduled_at == scheduled_at,
        Appointment.status.in_(["Pendiente", "Confirmada"]),
    )
    if exclude_id is not None:
        stmt = stmt.where(Appointment.id != exclude_id)
    if (await db.execute(stmt)).scalar_one_or_none() is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe una cita activa para esta fecha y hora")

@router.get("/patients", response_model=list[PatientRead])
async def patients(q: str | None = None, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    stmt = select(Patient).where(Patient.clinician_id == clinician_id).order_by(Patient.full_name)
    if q: stmt = stmt.where(Patient.full_name.ilike(f"%{q}%"))
    return (await db.execute(stmt)).scalars().all()

@router.post("/patients", response_model=PatientRead, status_code=201)
async def create_patient(data: PatientCreate, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    values = data.model_dump()
    values["full_name"] = patient_display_name(values)
    item = Patient(**values, clinician_id=clinician_id); db.add(item); await db.commit(); await db.refresh(item); return item

@router.get("/patients/{patient_id}", response_model=PatientRead)
async def patient(patient_id: int, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    return await owned_patient(patient_id, clinician_id, db)

@router.patch("/patients/{patient_id}", response_model=PatientRead)
async def update_patient(patient_id: int, data: PatientUpdate, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    item = await owned_patient(patient_id, clinician_id, db)
    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(item, field, value)
    if any(field in changes for field in PATIENT_NAME_FIELDS):
        values = {field: getattr(item, field) for field in PATIENT_NAME_FIELDS}
        # A client can submit the legacy full_name together with the structured
        # fields. Use that value as fallback so both representations stay in sync.
        item.full_name = patient_display_name(values, changes.get("full_name", item.full_name))
    await db.commit()
    await db.refresh(item)
    return item

@router.put("/patients/{patient_id}", response_model=PatientRead)
async def replace_patient(patient_id: int, data: PatientUpdate, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    return await update_patient(patient_id, data, clinician_id, db)

@router.get("/patients/{patient_id}/sessions", response_model=list[ClinicalSessionRead])
async def patient_sessions(patient_id: int, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    await owned_patient(patient_id, clinician_id, db)
    return (await db.execute(select(ClinicalSession).where(ClinicalSession.patient_id == patient_id, ClinicalSession.clinician_id == clinician_id).order_by(ClinicalSession.created_at.desc()))).scalars().all()

@router.post("/sessions", response_model=ClinicalSessionRead, status_code=201)
async def create_session(data: ClinicalSessionCreate, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    await owned_patient(data.patient_id, clinician_id, db)
    item = ClinicalSession(**data.model_dump(), clinician_id=clinician_id); db.add(item); await db.commit(); await db.refresh(item); return item

@router.get("/appointments", response_model=list[AppointmentRead])
async def appointments(patient_id: int | None = None, appointment_status: str | None = None, from_date: datetime | None = None, to_date: datetime | None = None, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    stmt = select(Appointment).where(Appointment.clinician_id == clinician_id)
    if patient_id is not None: stmt = stmt.where(Appointment.patient_id == patient_id)
    if appointment_status is not None: stmt = stmt.where(Appointment.status == appointment_status)
    if from_date is not None: stmt = stmt.where(Appointment.scheduled_at >= from_date)
    if to_date is not None: stmt = stmt.where(Appointment.scheduled_at <= to_date)
    return (await db.execute(stmt.order_by(Appointment.scheduled_at))).scalars().all()

@router.get("/appointments/{appointment_id}", response_model=AppointmentRead)
async def appointment(appointment_id: int, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    return await owned_appointment(appointment_id, clinician_id, db)

@router.post("/appointments", response_model=AppointmentRead, status_code=201)
async def create_appointment(data: AppointmentCreate, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    await owned_patient(data.patient_id, clinician_id, db)
    if data.status in {"Pendiente", "Confirmada"}: await ensure_available(data.scheduled_at, clinician_id, db)
    item = Appointment(**data.model_dump(), clinician_id=clinician_id); db.add(item); await db.commit(); await db.refresh(item); return item

@router.patch("/appointments/{appointment_id}", response_model=AppointmentRead)
async def update_appointment(appointment_id: int, data: AppointmentUpdate, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    item = await owned_appointment(appointment_id, clinician_id, db)
    changes = data.model_dump(exclude_unset=True)
    if "patient_id" in changes: await owned_patient(changes["patient_id"], clinician_id, db)
    scheduled_at = changes.get("scheduled_at", item.scheduled_at)
    appointment_status = changes.get("status", item.status)
    if appointment_status in {"Pendiente", "Confirmada"} and ("scheduled_at" in changes or "status" in changes):
        await ensure_available(scheduled_at, clinician_id, db, appointment_id)
    for field, value in changes.items(): setattr(item, field, value)
    await db.commit(); await db.refresh(item); return item

@router.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: int, clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    item = await owned_appointment(appointment_id, clinician_id, db)
    await db.delete(item); await db.commit()

@router.get("/dashboard")
async def dashboard(clinician_id: str = Depends(clinician), db: AsyncSession = Depends(get_db)):
    patients_count = (await db.execute(select(func.count(Patient.id)).where(Patient.clinician_id == clinician_id))).scalar_one()
    now = datetime.now(timezone.utc)
    appointments_count = (await db.execute(select(func.count(Appointment.id)).where(
        Appointment.clinician_id == clinician_id,
        Appointment.scheduled_at >= now,
        Appointment.status.in_(["Pendiente", "Confirmada"]),
    ))).scalar_one()
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
