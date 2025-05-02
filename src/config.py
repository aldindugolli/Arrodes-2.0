from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Ollama Settings
    OLLAMA_API_URL: str = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = "dolphin"
    
    # Security Settings
    ALLOWED_ORIGINS: list = ["http://localhost:8000", "http://localhost:3000"]
    
    # System Settings
    MAX_CONCURRENT_TASKS: int = 5
    LOG_LEVEL: str = "INFO"
    
    class Config:
        case_sensitive = True

settings = Settings() 