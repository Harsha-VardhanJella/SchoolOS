import os
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    APP_NAME: str = "SchoolOS API"
    ENV: str = "dev"
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_EXPIRES_MINUTES: int = 30
    JWT_EXPIRES_REFRESH: int=7
    CORS_ORIGINS: str = "http://localhost:5173"

    class Config:
        env_file = ENV_FILE
        case_sensitive = True

settings = Settings()
print("DEBUG: ENV FILE PATH =", ENV_FILE)
