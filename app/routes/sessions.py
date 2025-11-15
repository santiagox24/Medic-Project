from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.sessions import Session
from models.user import User
from schemas.sessions import SessionCreate, SessionRead
from datetime import datetime, timezone

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=SessionRead)
async def create_session(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db),
):
    # ✅ Aseguramos que la fecha tenga zona horaria UTC
    if session_data.date.tzinfo is None:
        session_data.date = session_data.date.replace(tzinfo=timezone.utc)
    else:
        session_data.date = session_data.date.astimezone(timezone.utc)

    new_session = Session(
        user_id=session_data.user_id,  # probablemente luego lo saques de un token o parámetro
        date=session_data.date,
        #analysis=session_data.analysis,
    )

    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

    return new_session

