from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    X_SECRET_KEY: str
    GROUP_ID: str
    CHANNEL_ID: str
    API_HOST: str
    PAYMENT_TOKEN: str
    SHOPID: str
    SHOPARTICLED: str
    TABLE_FILENAME: str

    class Config:
        __file_dir = Path(__file__).resolve().parent
        env_file = f"{__file_dir}/.env"


config = Settings()
