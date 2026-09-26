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
        # Patient registration was expanded from a minimal clinical record to
        # the administrative and demographic details used in the intake form.
        patient_columns = (
            ("document_type", "VARCHAR(16)"),
            ("first_name", "VARCHAR(80)"),
            ("second_name", "VARCHAR(80)"),
            ("first_surname", "VARCHAR(80)"),
            ("second_surname", "VARCHAR(80)"),
            ("gender", "VARCHAR(64)"),
            ("email", "VARCHAR(255)"),
            ("status", "VARCHAR(32) DEFAULT 'Activo'"),
            ("site", "VARCHAR(128)"),
            ("city", "VARCHAR(128)"),
            ("address", "VARCHAR(255)"),
            ("regime", "VARCHAR(64)"),
            ("administrator", "VARCHAR(160)"),
            ("marital_status", "VARCHAR(64)"),
            ("ethnic_group", "VARCHAR(128)"),
            ("population_group", "VARCHAR(128)"),
            ("occupation", "VARCHAR(128)"),
            ("education_level", "VARCHAR(128)"),
            ("zone", "VARCHAR(32)"),
            ("stratum", "VARCHAR(16)"),
            ("religion", "VARCHAR(128)"),
        )
        for name, definition in patient_columns:
            await conn.execute(text(f"ALTER TABLE patients ADD COLUMN IF NOT EXISTS {name} {definition}"))
