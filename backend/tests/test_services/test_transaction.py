"""Tests for TransactionService."""
from datetime import date, datetime, UTC

import pytest
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.services.transaction import TransactionService


def test_create_transaction(db_session: Session):
    svc = TransactionService()
    data = TransactionCreate(
        date=date(2026, 6, 15),
        description="Test sale",
        amount=100.50,
        notes="Optional note",
    )
    txn = svc.create(db_session, data)

    assert txn.id is not None
    assert txn.date == "2026-06-15"
    assert txn.description == "Test sale"
    assert txn.amount == 100.50
    assert txn.notes == "Optional note"
    assert txn.deleted_at is None


def test_create_transaction_minimal(db_session: Session):
    svc = TransactionService()
    data = TransactionCreate(
        date=date(2026, 6, 15),
        description="Minimal",
        amount=10.0,
    )
    txn = svc.create(db_session, data)
    assert txn.notes is None


def test_get_by_id_found(db_session: Session):
    svc = TransactionService()
    data = TransactionCreate(date=date(2026, 6, 15), description="Test", amount=50.0)
    created = svc.create(db_session, data)

    fetched = svc.get_by_id(db_session, created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.description == "Test"


def test_get_by_id_not_found(db_session: Session):
    svc = TransactionService()
    assert svc.get_by_id(db_session, "nonexistent-id") is None


def test_get_by_id_soft_deleted(db_session: Session):
    svc = TransactionService()
    data = TransactionCreate(date=date(2026, 6, 15), description="To delete", amount=30.0)
    txn = svc.create(db_session, data)

    svc.delete(db_session, txn.id)
    assert svc.get_by_id(db_session, txn.id) is None


def test_list_empty(db_session: Session):
    svc = TransactionService()
    transactions, total = svc.list(db_session)
    assert transactions == []
    assert total == 0


def test_list_pagination(db_session: Session):
    svc = TransactionService()
    for i in range(5):
        svc.create(db_session, TransactionCreate(
            date=date(2026, 6, 1),
            description=f"Item {i}",
            amount=float(i + 1),
        ))

    # Page 1, limit 2
    transactions, total = svc.list(db_session, page=1, limit=2)
    assert len(transactions) == 2
    assert total == 5

    # Page 3, limit 2
    transactions, total = svc.list(db_session, page=3, limit=2)
    assert len(transactions) == 1
    assert total == 5


def test_list_search(db_session: Session):
    svc = TransactionService()
    svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Apple sale", amount=10.0))
    svc.create(db_session, TransactionCreate(date=date(2026, 6, 2), description="Banana sale", amount=20.0))

    transactions, total = svc.list(db_session, search="apple")
    assert total == 1
    assert transactions[0].description == "Apple sale"

    transactions, total = svc.list(db_session, search="SALE")
    assert total == 2


def test_list_date_filter(db_session: Session):
    svc = TransactionService()
    svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Early", amount=10.0))
    svc.create(db_session, TransactionCreate(date=date(2026, 6, 15), description="Middle", amount=20.0))
    svc.create(db_session, TransactionCreate(date=date(2026, 7, 1), description="Late", amount=30.0))

    transactions, total = svc.list(db_session, from_date="2026-06-10", to_date="2026-06-30")
    assert total == 1
    assert transactions[0].description == "Middle"


def test_list_soft_deleted_excluded(db_session: Session):
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Soon gone", amount=10.0))
    svc.create(db_session, TransactionCreate(date=date(2026, 6, 2), description="Keep me", amount=20.0))

    svc.delete(db_session, txn.id)

    transactions, total = svc.list(db_session)
    assert total == 1
    assert transactions[0].description == "Keep me"


def test_update_transaction(db_session: Session):
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Original", amount=100.0))

    updated = svc.update(db_session, txn.id, TransactionUpdate(description="Updated", amount=200.0))
    assert updated is not None
    assert updated.description == "Updated"
    assert updated.amount == 200.0
    # Date unchanged
    assert updated.date == "2026-06-01"


def test_update_not_found(db_session: Session):
    svc = TransactionService()
    assert svc.update(db_session, "nonexistent", TransactionUpdate(description="Nope")) is None


def test_update_soft_deleted(db_session: Session):
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Gone", amount=10.0))
    svc.delete(db_session, txn.id)
    assert svc.update(db_session, txn.id, TransactionUpdate(description="Nope")) is None


def test_delete_transaction(db_session: Session):
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Delete me", amount=50.0))

    assert svc.delete(db_session, txn.id) is True

    # Verify soft delete
    db_session.refresh(txn)
    assert txn.deleted_at is not None


def test_delete_not_found(db_session: Session):
    svc = TransactionService()
    assert svc.delete(db_session, "nonexistent") is False


def test_delete_twice(db_session: Session):
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Twice", amount=10.0))
    assert svc.delete(db_session, txn.id) is True
    assert svc.delete(db_session, txn.id) is False


def test_to_response(db_session: Session):
    svc = TransactionService()
    data = TransactionCreate(date=date(2026, 6, 15), description="Response test", amount=75.0)
    txn = svc.create(db_session, data)

    resp = svc.to_response(txn)
    assert resp.id == txn.id
    assert resp.date == "2026-06-15"
    assert resp.description == "Response test"
    assert resp.amount == 75.0
    assert resp.invoice_number is None
    assert resp.notes is None
    assert isinstance(resp.created_at, str)
    assert isinstance(resp.updated_at, str)
