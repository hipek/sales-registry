from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class SellerInfo(BaseModel):
    name: str
    address: str
    nip: Optional[str] = None


class InvoiceItem(BaseModel):
    model_config = ConfigDict(json_encoders={Decimal: float})

    description: str
    quantity: int = 1
    unit: str = "szt."
    unit_price: Decimal
    total: Decimal


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(json_encoders={Decimal: float})

    invoice_number: str
    issue_date: str
    seller: SellerInfo
    items: List[InvoiceItem]
    total: Decimal
