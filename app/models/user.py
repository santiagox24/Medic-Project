from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.orm import Mapped,mapped_column
from typing import List

class User(Base):
    __tablename__ = "users"

    document_id : Mapped[str] = mapped_column(String,primary_key=True)
    username : Mapped[str] = mapped_column(unique=True)
    hashed_password : Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column(String)
    email : Mapped[str] = mapped_column(unique=True)
    tel : Mapped[str] = mapped_column(unique=True)
    age : Mapped[int] = mapped_column()
    gender : Mapped[str] = mapped_column()
    address : Mapped[str] = mapped_column()
    city : Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column()

   
                                                    