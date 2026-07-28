from datetime import UTC, datetime
import uuid

from sqlalchemy import Column, DateTime, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(String, nullable=False)  # ISO date "YYYY-MM-DD"
    description = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)  # Gross PLN
    invoice_number = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
