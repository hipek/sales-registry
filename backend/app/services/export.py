"""CSV export service."""
import csv
from io import StringIO
from typing import Optional

from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.services.transaction import TransactionService


def export_transactions_csv(
    db: Session,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> str:
    """Generate CSV string with UTF-8 BOM for all matching transactions."""
    service = TransactionService()
    transactions, _total = service.list(db, 1, 10000, None, from_date, to_date)

    output = StringIO()
    output.write("\ufeff")  # UTF-8 BOM for Excel
    writer = csv.writer(output)
    writer.writerow(["date", "description", "amount", "invoice_number", "notes"])
    for t in transactions:
        writer.writerow([t.date, t.description, t.amount, t.invoice_number, t.notes])

    return output.getvalue()
