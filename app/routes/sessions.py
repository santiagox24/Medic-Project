from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.sessions import Session
from schemas.sessions import SessionCreate, SessionRead
from services.llm import generate_text
from services.embeddings import get_embedding
from datetime import datetime, timezone

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=SessionRead)
async def create_session(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db),
):
    # Ensure UTC timezone
    if session_data.date.tzinfo is None:
        session_data.date = session_data.date.replace(tzinfo=timezone.utc)
    else:
        session_data.date = session_data.date.astimezone(timezone.utc)

    # 1. Generate embedding for the question
    q_vector = await get_embedding(session_data.question) if session_data.question else None

    # 2. Generate answer using LLM if a question was provided
    answer_text = None
    a_vector = None
    if session_data.question:
        prompt = f"Actúa como un asistente médico profesional. Responde a la siguiente consulta del paciente de manera clara y empática: {session_data.question}"
        answer_text = await generate_text(prompt)
        # 3. Generate embedding for the AI's answer
        a_vector = await get_embedding(answer_text)

    new_session = Session(
        user_id=session_data.user_id,
        date=session_data.date,
        question=session_data.question,
        question_vector=q_vector,
        answer=answer_text,
        answer_vector=a_vector,
        analysis=answer_text # For now, we use the same text as analysis or could be separate
    )

    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

    return new_session


