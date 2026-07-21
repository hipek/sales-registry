from datetime import datetime, UTC

from sqlalchemy import Column, String, Integer, DateTime
from app.models.transaction import Base


class Counter(Base):
    __tablename__ = "counters"

    id = Column(String, primary_key=True)  # e.g. "receipt-2026"
    value = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
