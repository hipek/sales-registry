from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.counter import Counter
from app.schemas.invoice import InvoiceResponse, SellerInfo, InvoiceItem
from app.utils.date import get_current_quarter


class InvoiceService:
    @staticmethod
    def get_invoice(db: Session, transaction: Transaction, settings) -> InvoiceResponse:
        # Get or create counter for current year
        year = transaction.date[:4]
        counter_id = f"receipt-{year}"
        counter = db.query(Counter).filter(Counter.id == counter_id).first()
        if not counter:
            counter = Counter(id=counter_id, value=0)
            db.add(counter)
            db.commit()
            db.refresh(counter)

        # Increment counter
        counter.value += 1
        db.commit()

        invoice_number = f"{settings.receipt_prefix}/{year}/{counter.value:03d}"

        seller = SellerInfo(
            name=settings.seller_name,
            address=settings.seller_address,
            nip=settings.seller_nip,
        )

        item = InvoiceItem(
            description=transaction.description,
            quantity=1,
            unit="szt.",
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
