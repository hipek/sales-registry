from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    database_url: str
    seller_name: str
    seller_address: str
    seller_nip: str | None = None
    quarterly_limit: float = 10813.50
    receipt_prefix: str = "R"
    receipt_unit: str = "szt."
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
