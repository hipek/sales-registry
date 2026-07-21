"""Tests for LimitService."""
from datetime import date

from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.services.limit import LimitService
from app.services.transaction import TransactionService
from app.schemas.transaction import TransactionCreate


def _create_txn(db: Session, day: int, amount: float, month: int = 7):
    svc = TransactionService()
    svc.create(db, TransactionCreate(
        date=date(2026, month, day),
        description=f"Sale {amount}",
        amount=amount,
    ))


def test_get_current_no_transactions(db_session: Session):
    svc = LimitService()
    result = svc.get_current(db_session, 10813.50)

    assert result.limit == 10813.50
    assert result.used == 0.0
    assert result.remaining == 10813.50
    assert result.is_exceeded is False
    assert result.year is not None
    assert 1 <= result.quarter <= 4


def test_get_current_with_usage(db_session: Session):
    _create_txn(db_session, 1, 1000.0)
    _create_txn(db_session, 15, 500.50)
    _create_txn(db_session, 20, 200.0)

    svc = LimitService()
    result = svc.get_current(db_session, 10813.50)

    assert result.used == 1700.50
    assert result.remaining == 9113.0
    assert result.is_exceeded is False


def test_get_current_exceeded(db_session: Session):
    _create_txn(db_session, 1, 5000.0)
    _create_txn(db_session, 10, 6000.0)

    svc = LimitService()
    result = svc.get_current(db_session, 10000.0)

    assert result.used == 11000.0
    assert result.remaining == 0.0
    assert result.is_exceeded is True


def test_get_current_excludes_soft_deleted(db_session: Session):
    _create_txn(db_session, 1, 1000.0)

    # Create then soft-delete a transaction
    txn_svc = TransactionService()
    txn = txn_svc.create(db_session, TransactionCreate(
        date=date(2026, 7, 2),
        description="To delete",
        amount=5000.0,
    ))
    txn_svc.delete(db_session, txn.id)

    svc = LimitService()
    result = svc.get_current(db_session, 10813.50)

    assert result.used == 1000.0
