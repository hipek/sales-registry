from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.schemas.invoice import InvoiceResponse
from app.services.invoice import InvoiceService
from app.utils.pdf import generate_receipt_pdf, sanitize_filename

router = APIRouter()


@router.get("/{transaction_id}", response_model=InvoiceResponse)
def get_invoice(transaction_id: str, db: Session = Depends(get_db)):
    service = InvoiceService()
    invoice = service.get_or_create_invoice(db, transaction_id, settings)
    return invoice


@router.get("/{transaction_id}/download")
def download_invoice(transaction_id: str, db: Session = Depends(get_db)):
    service = InvoiceService()
    invoice = service.get_or_create_invoice(db, transaction_id, settings)

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
        headers={"Content-Disposition": f"attachment; filename={sanitize_filename(invoice.invoice_number)}.pdf"},
    )
