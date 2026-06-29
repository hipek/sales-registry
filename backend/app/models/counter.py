from sqlalchemy import Column, String, Integer
from app.models.transaction import Base


class Counter(Base):
    __tablename__ = "counters"

    id = Column(String, primary_key=True)  # e.g. "receipt-2026"
    value = Column(Integer, nullable=False, default=0)
