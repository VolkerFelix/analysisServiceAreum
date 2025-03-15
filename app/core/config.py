import os
from typing import List
from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "Areum Health Analysis Service"
    PROJECT_DESCRIPTION: str = "AI-powered health analysis for Areum Health"
    VERSION: str = "0.1.0"

    API_PREFIX: str = "/api"
    SHOW_DOCS: bool = True

    ALLOWED_ORIGINS: List[AnyHttpUrl] = []

    # Database config for potential future use
    DATABASE_URL: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
