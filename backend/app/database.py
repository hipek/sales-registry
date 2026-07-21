from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


@lru_cache(maxsize=1)
def get_engine():
    return create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},  # SQLite-specific
    )


SessionLocal = sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
