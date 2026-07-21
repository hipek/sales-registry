from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.limit import QuarterlyLimitResponse
from app.utils.date import get_current_quarter, get_quarter_date_range


class LimitService:
    @staticmethod
    def get_current(db: Session, quarterly_limit: float) -> QuarterlyLimitResponse:
        year, quarter = get_current_quarter()
        start_date, end_date = get_quarter_date_range(year, quarter)

        used = (
            db.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(
                Transaction.date >= start_date.isoformat(),
                Transaction.date <= end_date.isoformat(),
                Transaction.deleted_at.is_(None),
            )
            .scalar()
        )
        used = float(used) if used else 0.0
        remaining = max(0, quarterly_limit - used)

        return QuarterlyLimitResponse(
            year=year,
            quarter=quarter,
            limit=quarterly_limit,
            used=round(used, 2),
            remaining=round(remaining, 2),
            is_exceeded=used > quarterly_limit,
        )
