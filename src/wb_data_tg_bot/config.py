from pathlib import Path
from typing import Optional, Literal

from pydantic import constr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "WbDataTgBot"
    PROJECT_DESCRIPTION: str = "WbDataTgBot for WbDataService"
    VERSION: str = "0.0.1"
    API_SERVERS: list = [
        {
            "url": "http://localhost:8000",
            "description": "Local server"
        },
        {
            "url": "https://poorly-ideal-cobra.ngrok-free.app",  # My free ngrok domain
            "description": "Ngrok free server"
        }
    ]

    LOGGER_NAME: str = "wb_data_tg_bot_logger"
    LOG_LEVEL: str = "info"
    LOG_FILENAME: str = "wb_data.log"

    TELEGRAM_BOT_MODE: Literal["webhook", "pulling"] = "pulling"
    TELEGRAM_BOT_WEBHOOK_URL: Optional[str] = None
    TELEGRAM_BOT_PULLING_DELAY_SECONDS: float = 0.1
    TELEGRAM_BOT_TOKEN: constr(pattern=r"^\d{10}:[a-zA-Z0-9_-]{35}$")

    BACKEND_CORS_ORIGINS: list[str] = ["http://127.0.0.1:8000",
                                       "http://localhost:8000",
                                       "https://poorly-ideal-cobra.ngrok-free.app"]
    SERVER_PORT: int = 8001

    def get_db_url(self):
        return (f"{self.DB_SCHEMA}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?ssl={self.DB_SSL}")

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"
        extra = "ignore"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
