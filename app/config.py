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
# Vision and tool calling support PDF/image attachments in the copilot.
# Set MODEL_NAME in the environment to override this default.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.2")

ICD11_API_URL = os.getenv("ICD11_API_URL", "http://icd11:80").rstrip("/")
ICD11_RELEASE = os.getenv("ICD11_RELEASE", "2026-01")
ICD11_LANGUAGE = os.getenv("ICD11_LANGUAGE", "es")

# Local originals are mounted outside the application container.
ATTACHMENTS_DIR = os.getenv("ATTACHMENTS_DIR", "/code/storage/attachments")
ATTACHMENT_MAX_BYTES = int(os.getenv("ATTACHMENT_MAX_BYTES", str(20 * 1024 * 1024)))
