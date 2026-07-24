from datetime import datetime, UTC

from sqlalchemy import Column, String, DateTime
from app.models.transaction import Base


class CounterLock(Base):
    __tablename__ = "counter_locks"

    id = Column(String, primary_key=True)
    locked_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
