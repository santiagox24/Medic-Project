from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from database import Base
from datetime import datetime
from pgvector.sqlalchemy import Vector


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.document_id"))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=True)
    
    question: Mapped[str] = mapped_column(String, nullable=True)
    question_vector: Mapped[list] = mapped_column(Vector(1536), nullable=True)
    
    answer: Mapped[str] = mapped_column(String, nullable=True)
    answer_vector: Mapped[list] = mapped_column(Vector(1536), nullable=True)
    
    analysis: Mapped[str] = mapped_column(String, nullable=True)
    