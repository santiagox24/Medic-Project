from dotenv import load_dotenv
import os

load_dotenv()


# Database / auth
DATABASE_URL = os.getenv("POSTGRES_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
# Provide a safe default for token expiry minutes
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
# OpenAI / LLM configuration
# Set `MODEL_NAME` in environment to override the default model used by the app
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5-mini")

ICD11_API_URL = os.getenv("ICD11_API_URL", "http://icd11:80").rstrip("/")
ICD11_RELEASE = os.getenv("ICD11_RELEASE", "2026-01")
ICD11_LANGUAGE = os.getenv("ICD11_LANGUAGE", "es")
