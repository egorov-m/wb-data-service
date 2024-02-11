from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "WbDataService"
    PROJECT_DESCRIPTION: str = "Welcome to WbDataService's API documentation!"
    VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"
    API_SERVERS: list = [
        {
            "url": "http://localhost:8000",
            "description": "Local server"
        }
    ]

    LOGGER_NAME: str = "wb_data_logger"
    LOG_LEVEL: str = "info"
    LOG_FILENAME: str = "wb_data.log"

    DB_SCHEMA: str = "postgresql"
    DB_DRIVER: str = "asyncpg"
    DB_HOST: str = "wb_db"
    DB_PORT: str = "5432"
    DB_SSL: str = "prefer"  # disable, allow, prefer, require, verify-ca, verify-full
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "wb_db"

    DB_POOL_SIZE: int = 75
    DB_MAX_OVERFLOW: int = 20

    DB_METADATA_CREATE_ALL: bool = True

    BACKEND_CORS_ORIGINS: list[str] = ["http://127.0.0.1:8000",
                                       "http://localhost:8000"]

    def get_db_url(self):
        return (f"{self.DB_SCHEMA}+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?ssl={self.DB_SSL}")

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
