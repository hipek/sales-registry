from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class QuarterlyLimitResponse(BaseModel):
    model_config = ConfigDict(json_encoders={Decimal: float})

    year: int
    quarter: int
    limit: Decimal
    used: Decimal
    remaining: Decimal
    is_exceeded: bool
