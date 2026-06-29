from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.schemas.common import PaginatedResponse, ErrorResponse
from app.services.transaction import TransactionService

router = APIRouter()


@router.post("", response_model=TransactionResponse, status_code=201)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
):
    service = TransactionService()
    transaction = service.create(db, data)
    return service.to_response(transaction)


@router.get("/export")
def export_transactions(
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """Export transactions as CSV with UTF-8 BOM."""
    service = TransactionService()
    transactions, _total = service.list(db, 1, 10000, None, from_date, to_date)

    import csv
    from io import StringIO

    output = StringIO()
    output.write("\ufeff")  # UTF-8 BOM for Excel
    writer = csv.writer(output)
    writer.writerow(["date", "description", "amount", "invoice_number", "notes"])
    for t in transactions:
        writer.writerow([t.date, t.description, t.amount, t.invoice_number, t.notes])

    return output.getvalue()


@router.get("", response_model=PaginatedResponse[TransactionResponse])
def list_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
    db: Session = Depends(get_db),
):
    service = TransactionService()
    transactions, total = service.list(db, page, limit, search, from_date, to_date)
    data = [service.to_response(t) for t in transactions]
    total_pages = max(1, (total + limit - 1) // limit)
    return PaginatedResponse(
        data=data,
        meta={"page": page, "limit": limit, "total": total, "total_pages": total_pages},
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: str, db: Session = Depends(get_db)):
    service = TransactionService()
    transaction = service.get_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Transaction not found"})
    return service.to_response(transaction)


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: str,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
):
    service = TransactionService()
    transaction = service.get_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Transaction not found"})
    updated = service.update(db, transaction_id, data)
    return service.to_response(updated)


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: str, db: Session = Depends(get_db)):
    service = TransactionService()
    if not service.delete(db, transaction_id):
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Transaction not found"})
