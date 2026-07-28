from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: dict  # {"page": 1, "limit": 10, "total": 42, "total_pages": 5}


class ErrorResponse(BaseModel):
    error: dict  # {"code": "VALIDATION_ERROR", "message": "...", "details": [...]}
