import csv
from io import StringIO
from typing import Optional

from sqlalchemy.orm import Session

from app.services.transaction import TransactionService


def export_transactions_csv(
    db: Session,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> str:
    service = TransactionService()

    # Fetch all results in batches to avoid truncation
    all_transactions = []
    page = 1
    while True:
        batch, total = service.list(db, page, 1000, None, from_date, to_date)
        all_transactions.extend(batch)
        if len(all_transactions) >= total or not batch:
            break
        page += 1

    output = StringIO()
    output.write("\ufeff")
    writer = csv.writer(output)
    writer.writerow(["date", "description", "amount", "invoice_number", "notes"])
    for t in all_transactions:
        writer.writerow([t.date, t.description, t.amount, t.invoice_number, t.notes])

    return output.getvalue()
