from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class TransactionCreate(BaseModel):
    date: date
    description: str = Field(min_length=1, max_length=500)
    amount: float = Field(gt=0, le=1000000)
    notes: Optional[str] = None


class TransactionUpdate(BaseModel):
    date: Optional[date] = None
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    amount: Optional[float] = Field(None, gt=0, le=1000000)
    notes: Optional[str] = None


class TransactionResponse(BaseModel):
    id: str
    date: str
    description: str
    amount: float
    invoice_number: Optional[str] = None
    notes: Optional[str] = None
    created_at: str
    updated_at: str
