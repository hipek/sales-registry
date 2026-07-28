from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.serializers import DecimalMoneyMixin


class SellerInfo(BaseModel):
    name: str
    address: str
    nip: Optional[str] = None


class InvoiceItem(DecimalMoneyMixin, BaseModel):
    description: str
    quantity: int = 1
    unit: str = "szt."
    unit_price: Decimal
    total: Decimal


class InvoiceResponse(DecimalMoneyMixin, BaseModel):
    invoice_number: str
    issue_date: str
    seller: SellerInfo
    items: List[InvoiceItem]
    total: Decimal
