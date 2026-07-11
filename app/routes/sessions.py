from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.sessions import Session
from schemas.sessions import SessionCreate, SessionRead
from services.session_processor import process_new_session
from typing import List

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("/", response_model=List[SessionRead])
async def get_sessions(
    db: AsyncSession = Depends(get_db),
):
    """
    Returns a list of all clinical sessions ordered by date (newest first).
    """
    stmt = select(Session).order_by(Session.date.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Deletes a session by ID.
    """
    stmt = select(Session).where(Session.id == session_id)
    result = await db.execute(stmt)
    session = result.scalars().first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    await db.delete(session)
    await db.commit()
    return None


@router.post("/", response_model=SessionRead)
async def create_session(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Creates a new clinical session. 
    Internally generates embeddings and AI responses.
    """
    return await process_new_session(db, session_data)


