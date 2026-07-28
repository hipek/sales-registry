from decimal import Decimal
import os
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("DATA_DIR", str(BASE_DIR.parent / "data")))
DATABASE_PATH = DATA_DIR / "database.sqlite"


class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/database.sqlite"
    seller_name: str = "Jan Kowalski"
    seller_address: str = "ul. Testowa 1, 00-001 Warszawa"
    seller_nip: str | None = None
    quarterly_limit: Decimal = Decimal("10813.50")
    receipt_prefix: str = "R"
    receipt_unit: str = "szt."
    cors_origins: str = "http://localhost:3000,http://host.docker.internal:8000"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @model_validator(mode="after")
    def normalize_database_url(self) -> "Settings":
        if self.database_url.startswith("sqlite:///./"):
            self.database_url = f"sqlite:///{DATABASE_PATH}"
        return self

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
