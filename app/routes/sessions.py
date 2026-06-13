from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.sessions import SessionCreate, SessionRead
from services.session_processor import process_new_session

router = APIRouter(prefix="/sessions", tags=["sessions"])


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


