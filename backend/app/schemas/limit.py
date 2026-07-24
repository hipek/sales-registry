from decimal import Decimal

from pydantic import BaseModel


class QuarterlyLimitResponse(BaseModel):
    year: int
    quarter: int
    limit: Decimal
    used: Decimal
    remaining: Decimal
    is_exceeded: bool
