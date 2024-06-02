from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    X_SECRET_KEY: str
    ALLOWED_HOSTS: List[str]
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: str
    DEBUG: bool = False

    class Config:
        __file_dir = Path(__file__).resolve().parent
        env_file = f"{__file_dir}/.env"


config = Settings()
