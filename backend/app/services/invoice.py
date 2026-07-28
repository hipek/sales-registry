import threading
from typing import Optional, Protocol

from fastapi import HTTPException
from sqlalchemy import delete, insert, text, update
from sqlalchemy.orm import Session

from app.models.counter import Counter
from app.models.counter_lock import CounterLock
from app.models.transaction import Transaction
from app.schemas.invoice import InvoiceItem, InvoiceResponse, SellerInfo


class ReceiptSettings(Protocol):
    """Minimal contract for settings used in receipt generation."""

    receipt_prefix: str
    seller_name: str
    seller_address: str
    seller_nip: Optional[str]
    receipt_unit: str


_COUNTER_LOCKS: dict[str, threading.Lock] = {}
_COUNTER_LOCKS_GUARD = threading.Lock()


def _get_counter_lock(counter_id: str) -> threading.Lock:
    with _COUNTER_LOCKS_GUARD:
        lock = _COUNTER_LOCKS.get(counter_id)
        if lock is None:
            lock = threading.Lock()
            _COUNTER_LOCKS[counter_id] = lock
    return lock


class InvoiceService:
    @staticmethod
    def get_or_create_invoice(db: Session, transaction_id: str, settings: ReceiptSettings) -> InvoiceResponse:
        row = (
            db.execute(
                text("SELECT id, date, description, amount, invoice_number FROM transactions WHERE id = :id"),
                {"id": transaction_id},
            )
            .mappings()
            .first()
        )

        if row is None:
            raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Transaction not found"})

        invoice_number = row["invoice_number"]
        if not invoice_number:
            year = row["date"][:4]
            counter_id = f"receipt-{year}"

            with _get_counter_lock(counter_id):
                db.rollback()
                db.execute(text("BEGIN IMMEDIATE"))

                try:
                    lock_result = db.execute(insert(CounterLock).values(id=counter_id))
                    if lock_result.rowcount != 1:
                        db.rollback()
                        raise RuntimeError("Counter lock unavailable")

                    counter = db.query(Counter).with_for_update().filter(Counter.id == counter_id).first()
                    if counter is None:
                        counter = Counter(id=counter_id, value=0)
                        db.add(counter)
                        db.flush()

                    new_value = counter.value + 1
                    counter.value = new_value
                    db.flush()

                    invoice_number = f"{settings.receipt_prefix}/{year}/{new_value:03d}"
                    db.execute(
                        update(Transaction)
                        .where(Transaction.id == transaction_id)
                        .values(invoice_number=invoice_number)
                    )
                    db.commit()
                except Exception:
                    db.rollback()
                    raise
                else:
                    db.execute(delete(CounterLock).where(CounterLock.id == counter_id))
                    db.commit()

        seller = SellerInfo(
            name=settings.seller_name,
            address=settings.seller_address,
            nip=settings.seller_nip,
        )

        item = InvoiceItem(
            description=row["description"],
            quantity=1,
            unit=settings.receipt_unit,
            unit_price=row["amount"],
            total=row["amount"],
        )

        return InvoiceResponse(
            invoice_number=invoice_number,
            issue_date=row["date"],
            seller=seller,
            items=[item],
            total=row["amount"],
        )
