from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from config import DATABASE_URL
from models import Base

engine = create_async_engine(DATABASE_URL,echo=True)

async_session = sessionmaker(engine,expire_on_commit=False,class_=AsyncSession)


async def get_db():
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
        # The project does not use Alembic yet. Keep existing installations
        # compatible while adding the ICD-11 fields introduced after launch.
        await conn.execute(text("ALTER TABLE clinical_sessions ADD COLUMN IF NOT EXISTS diagnosis_code VARCHAR(32)"))
        await conn.execute(text("ALTER TABLE clinical_sessions ADD COLUMN IF NOT EXISTS diagnosis_uri VARCHAR(512)"))
        await conn.execute(text("ALTER TABLE clinical_sessions ADD COLUMN IF NOT EXISTS diagnosis_release VARCHAR(32)"))
        await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_clinical_sessions_diagnosis_code ON clinical_sessions (diagnosis_code)"))
