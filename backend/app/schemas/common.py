from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: dict  # {"page": 1, "limit": 10, "total": 42, "total_pages": 5}


class ErrorResponse(BaseModel):
    error: dict  # {"code": "VALIDATION_ERROR", "message": "...", "details": [...]}
