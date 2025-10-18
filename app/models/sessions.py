from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base
from datetime import datetime,timezone


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id: Mapped[str] = mappedcolumn(String,ForeignKey("users.document_id"))
    date : Mapped[datetime] = mappecolumn(DateTime,nullable=False)
    anylisis : Mapped[str] = mapped_column()
    users : Mapped["User"] = relationship(back_populates="sessions")