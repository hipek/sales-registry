from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.invoice import InvoiceResponse
from app.services.invoice import InvoiceService
from app.services.transaction import TransactionService
from app.utils.pdf import generate_receipt_pdf
from app.config import settings

router = APIRouter()


def _get_transaction_or_404(db: Session, transaction_id: str):
    svc = TransactionService()
    txn = svc.get_by_id(db, transaction_id)
    if not txn:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Transaction not found"})
    return txn


@router.get("/{transaction_id}", response_model=InvoiceResponse)
def get_invoice(transaction_id: str, db: Session = Depends(get_db)):
    transaction = _get_transaction_or_404(db, transaction_id)
    service = InvoiceService()
    invoice = service.get_invoice(db, transaction, settings)
    return invoice


@router.get("/{transaction_id}/download")
def download_invoice(transaction_id: str, db: Session = Depends(get_db)):
    transaction = _get_transaction_or_404(db, transaction_id)
    service = InvoiceService()
    invoice = service.get_invoice(db, transaction, settings)

    pdf_bytes = generate_receipt_pdf(
        invoice_number=invoice.invoice_number,
        issue_date=invoice.issue_date,
        seller_name=invoice.seller.name,
        seller_address=invoice.seller.address,
        seller_nip=invoice.seller.nip,
        description=invoice.items[0].description,
        amount=invoice.total,
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={invoice.invoice_number}.pdf"},
    )
