from decimal import Decimal

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class TransactionCreate(BaseModel):
    date: date
    description: str = Field(min_length=1, max_length=500)
    amount: Decimal = Field(gt=Decimal("0"), le=Decimal("1000000.00"))
    notes: Optional[str] = None


class TransactionUpdate(BaseModel):
    date: Optional[date] = None
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    amount: Optional[Decimal] = Field(None, gt=Decimal("0"), le=Decimal("1000000.00"))
    notes: Optional[str] = None


class TransactionResponse(BaseModel):
    id: str
    date: str
    description: str
    amount: Decimal
    invoice_number: Optional[str] = None
    notes: Optional[str] = None
    created_at: str
    updated_at: str
