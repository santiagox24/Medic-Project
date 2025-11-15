from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from database import Base
from datetime import datetime


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.document_id"))
    date : Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False)
    #analysis : Mapped[str] = mapped_column()