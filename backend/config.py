import os

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

_raw_database_url = os.getenv(
    "DATABASE_URL",
    "postgresql://brewmatch:brewmatch@localhost:5432/brewmatch",
)
# Hosted providers sometimes still emit the older postgres:// scheme.
DATABASE_URL = (
    _raw_database_url.replace("postgres://", "postgresql://", 1)
    if _raw_database_url.startswith("postgres://")
    else _raw_database_url
)

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "dev-only-change-this-in-production",
)
if (
    ENVIRONMENT == "production"
    and JWT_SECRET_KEY == "dev-only-change-this-in-production"
):
    raise RuntimeError("JWT_SECRET_KEY must be set to a strong secret in production")

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "true").lower() in {
    "1",
    "true",
    "yes",
}
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "12"))


def cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins or ["http://localhost:3000"]
