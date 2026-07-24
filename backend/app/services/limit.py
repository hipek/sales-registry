from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.limit import QuarterlyLimitResponse
from app.utils.date import get_current_quarter, get_quarter_date_range


class LimitService:
    @staticmethod
    def get_current(db: Session, quarterly_limit: Decimal) -> QuarterlyLimitResponse:
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
        used = Decimal(str(used)) if used else Decimal("0")
        remaining = max(Decimal("0"), quarterly_limit - used)

        return QuarterlyLimitResponse(
            year=year,
            quarter=quarter,
            limit=Decimal(str(quarterly_limit)),
            used=used,
            remaining=remaining,
            is_exceeded=used > quarterly_limit,
        )
