from typing import Optional, Protocol

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.counter import Counter
from app.schemas.invoice import InvoiceResponse, SellerInfo, InvoiceItem


class ReceiptSettings(Protocol):
    """Minimal contract for settings used in receipt generation."""
    receipt_prefix: str
    seller_name: str
    seller_address: str
    seller_nip: Optional[str]
    receipt_unit: str


class InvoiceService:
    @staticmethod
    def get_or_create_invoice(db: Session, transaction: Transaction, settings: ReceiptSettings) -> InvoiceResponse:
        if transaction.invoice_number:
            invoice_number = transaction.invoice_number
        else:
            year = transaction.date[:4]
            counter_id = f"receipt-{year}"

            # Atomic increment — prevents duplicate invoice numbers under concurrency
            result = db.execute(
                update(Counter)
                .where(Counter.id == counter_id)
                .values(value=Counter.value + 1)
            )
            if result.rowcount == 0:
                # Counter doesn't exist yet — insert with value 1
                counter = Counter(id=counter_id, value=1)
                db.add(counter)
                db.flush()  # assigns without committing
                new_value = 1
            else:
                new_value = db.query(Counter.value).filter(Counter.id == counter_id).scalar()

            invoice_number = f"{settings.receipt_prefix}/{year}/{new_value:03d}"
            transaction.invoice_number = invoice_number
            db.commit()

        seller = SellerInfo(
            name=settings.seller_name,
            address=settings.seller_address,
            nip=settings.seller_nip,
        )

        item = InvoiceItem(
            description=transaction.description,
            quantity=1,
            unit=settings.receipt_unit,
            unit_price=transaction.amount,
            total=transaction.amount,
        )

        return InvoiceResponse(
            invoice_number=invoice_number,
            issue_date=transaction.date,
            seller=seller,
            items=[item],
            total=transaction.amount,
        )
