from fastapi import FastAPI
from routes import auth, user,sessions
from database import init_db
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="medic project", lifespan=lifespan)

origins =[
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

@app.get("/")
def read_root():
    return{"Hello" : "world"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(sessions.router)
