from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, String

from app.models.transaction import Base


class CounterLock(Base):
    __tablename__ = "counter_locks"

    id = Column(String, primary_key=True)
    locked_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
