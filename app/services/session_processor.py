from sqlalchemy.ext.asyncio import AsyncSession
from models.sessions import Session
from schemas.sessions import SessionCreate
from services.llm import generate_text
from services.embeddings import get_embedding
from datetime import datetime, timezone

async def process_new_session(db: AsyncSession, session_data: SessionCreate) -> Session:
    """
    Handles the full workflow for a new clinical session:
    1. Normalizes date.
    2. Generates question embedding.
    3. Obtains AI response/analysis.
    4. Generates answer embedding.
    5. Saves and returns the complete session.
    """
    # Ensure UTC timezone
    if session_data.date.tzinfo is None:
        session_data.date = session_data.date.replace(tzinfo=timezone.utc)
    else:
        session_data.date = session_data.date.astimezone(timezone.utc)

    # 1. Generate embedding for the question
    q_vector = await get_embedding(session_data.question) if session_data.question else None

    # 2. Generate answer using LLM
    answer_text = None
    a_vector = None
    if session_data.question:
        prompt = (
            "Actúa como un asistente médico profesional. "
            "Responde a la siguiente consulta del paciente de manera clara, "
            f"empática y profesional: {session_data.question}"
        )
        answer_text = await generate_text(prompt)
        # 3. Generate embedding for AI answer
        a_vector = await get_embedding(answer_text)

    # 4. Create model instance
    new_session = Session(
        user_id=session_data.user_id,
        date=session_data.date,
        title=session_data.title,
        question=session_data.question,
        question_vector=q_vector,
        answer=answer_text,
        answer_vector=a_vector,
        analysis=answer_text # Could be expanded later
    )

    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    return new_session
