from dotenv import load_dotenv
import os

load_dotenv()


# Database / auth
DATABASE_URL = os.getenv("POSTGRES_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
# Provide a safe default for token expiry minutes
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCES_TOKEN_EXPIRE_MINUTES", "15"))
# OpenAI / LLM configuration
# Set `MODEL_NAME` in environment to override the default model used by the app
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5-mini")