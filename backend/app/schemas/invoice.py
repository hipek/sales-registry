from pydantic import BaseModel
from typing import List, Optional


class SellerInfo(BaseModel):
    name: str
    address: str
    nip: Optional[str] = None


class InvoiceItem(BaseModel):
    description: str
    quantity: int = 1
    unit: str = "szt."
    unit_price: float
    total: float


class InvoiceResponse(BaseModel):
    invoice_number: str
    issue_date: str
    seller: SellerInfo
    items: List[InvoiceItem]
    total: float
