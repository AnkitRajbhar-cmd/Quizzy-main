import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017/pdf_quiz_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Make GOOGLE_API_KEY optional to avoid startup failure when not set
    GOOGLE_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
