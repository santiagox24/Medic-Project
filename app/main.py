from fastapi import FastAPI
from routes import auth, user,sessions
from database import init_db
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Medic Project API",
    description="Asistente médico con capacidades de búsqueda vectorial e IA.",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:5173",
    "http://0.0.0.0:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["root"])
def read_root():
    return {
        "project": "Medic Project API",
        "status": "online",
        "features": ["Auth", "Vector Search", "LLM Integration"]
    }

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(sessions.router)
