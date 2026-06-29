from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/database.sqlite"
    seller_name: str = ""
    seller_address: str = ""
    seller_nip: str | None = None
    quarterly_limit: float = 10813.50
    receipt_prefix: str = "R"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
    )


settings = Settings()
