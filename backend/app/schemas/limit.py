from decimal import Decimal

from pydantic import BaseModel

from app.schemas.serializers import DecimalMoneyMixin


class QuarterlyLimitResponse(DecimalMoneyMixin, BaseModel):
    year: int
    quarter: int
    limit: Decimal
    used: Decimal
    remaining: Decimal
    is_exceeded: bool
