from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.limit import QuarterlyLimitResponse
from app.services.limit import LimitService
from app.config import settings

router = APIRouter()


@router.get("/current", response_model=QuarterlyLimitResponse)
def get_current_limit(db: Session = Depends(get_db)):
    service = LimitService()
    return service.get_current(db, settings.quarterly_limit)
