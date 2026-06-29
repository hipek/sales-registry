from pydantic import BaseModel


class QuarterlyLimitResponse(BaseModel):
    year: int
    quarter: int
    limit: float
    used: float
    remaining: float
    is_exceeded: bool
