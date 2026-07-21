from datetime import date, datetime, UTC
from typing import Optional
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse


class TransactionService:
    @staticmethod
    def create(db: Session, data: TransactionCreate) -> Transaction:
        now = datetime.now(UTC)
        transaction = Transaction(
            date=data.date.isoformat(),
            description=data.description,
            amount=data.amount,
            notes=data.notes,
            created_at=now,
            updated_at=now,
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def get_by_id(db: Session, transaction_id: str) -> Optional[Transaction]:
        return (
            db.query(Transaction)
            .filter(Transaction.id == transaction_id, Transaction.deleted_at.is_(None))
            .first()
        )

    @staticmethod
    def list(
        db: Session,
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> tuple[list[Transaction], int]:
        query = db.query(Transaction).filter(Transaction.deleted_at.is_(None))

        if search:
            # Escape LIKE metacharacters to prevent pattern injection
            escaped = search.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')
            query = query.filter(
                Transaction.description.ilike(f"%{escaped}%", escape='\\')
            )
        if from_date:
            query = query.filter(Transaction.date >= from_date)
        if to_date:
            query = query.filter(Transaction.date <= to_date)

        total = query.count()
        transactions = (
            query.order_by(Transaction.date.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )
        return transactions, total

    @staticmethod
    def update(db: Session, transaction_id: str, data: TransactionUpdate) -> Optional[Transaction]:
        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id, Transaction.deleted_at.is_(None)
        ).first()
        if not transaction:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(transaction, key, value)
        transaction.updated_at = datetime.now(UTC)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def delete(db: Session, transaction_id: str) -> bool:
        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id, Transaction.deleted_at.is_(None)
        ).first()
        if not transaction:
            return False
        transaction.deleted_at = datetime.now(UTC)
        db.commit()
        return True

    @staticmethod
    def to_response(transaction: Transaction) -> TransactionResponse:
        return TransactionResponse(
            id=transaction.id,
            date=transaction.date,
            description=transaction.description,
            amount=transaction.amount,
            invoice_number=transaction.invoice_number,
            notes=transaction.notes,
            created_at=transaction.created_at.isoformat(),
            updated_at=transaction.updated_at.isoformat(),
        )
