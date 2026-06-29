from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.counter import Counter
from app.schemas.invoice import InvoiceResponse, SellerInfo, InvoiceItem


class InvoiceService:
    @staticmethod
    def get_invoice(db: Session, transaction: Transaction, settings) -> InvoiceResponse:
        # Reuse existing invoice_number if already assigned
        if transaction.invoice_number:
            invoice_number = transaction.invoice_number
        else:
            # Generate new invoice number
            year = transaction.date[:4]
            counter_id = f"receipt-{year}"
            counter = db.query(Counter).filter(Counter.id == counter_id).first()
            if not counter:
                counter = Counter(id=counter_id, value=0)
                db.add(counter)
                db.commit()
                db.refresh(counter)

            counter.value += 1
            invoice_number = f"{settings.receipt_prefix}/{year}/{counter.value:03d}"

            # Persist invoice_number on transaction
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
