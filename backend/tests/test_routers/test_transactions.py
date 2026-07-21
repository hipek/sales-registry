"""Tests for transaction API endpoints."""
from datetime import date, UTC, datetime
import uuid

from fastapi.testclient import TestClient

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.transaction import TransactionService
from app.utils.date import get_current_quarter


def test_create_transaction(client: TestClient, db_session):
    resp = client.post("/api/transactions", json={
        "date": "2026-06-15",
        "description": "Test sale",
        "amount": 100.50,
        "notes": "Some notes",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["description"] == "Test sale"
    assert data["amount"] == 100.50
    assert data["notes"] == "Some notes"
    assert data["id"] is not None
    assert data["invoice_number"] is None


def test_create_transaction_validation_error(client: TestClient, db_session):
    resp = client.post("/api/transactions", json={
        "date": "2026-06-15",
        "description": "",
        "amount": -5,
    })
    assert resp.status_code == 400
    data = resp.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_create_transaction_missing_field(client: TestClient, db_session):
    resp = client.post("/api/transactions", json={
        "date": "2026-06-15",
        "amount": 50.0,
    })
    assert resp.status_code == 400
    data = resp.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_list_transactions_empty(client: TestClient, db_session):
    resp = client.get("/api/transactions")
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"] == []
    assert data["meta"]["total"] == 0
    assert data["meta"]["page"] == 1


def test_list_transactions_pagination(client: TestClient, db_session):
    svc = TransactionService()
    for i in range(3):
        svc.create(db_session, TransactionCreate(
            date=date(2026, 6, i + 1),
            description=f"Item {i}",
            amount=float(i + 1) * 10,
        ))

    resp = client.get("/api/transactions?page=1&limit=2")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["data"]) == 2
    assert data["meta"]["total"] == 3
    assert data["meta"]["total_pages"] == 2


def test_list_transactions_search(client: TestClient, db_session):
    svc = TransactionService()
    svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Widget sale", amount=10.0))
    svc.create(db_session, TransactionCreate(date=date(2026, 6, 2), description="Gadget sale", amount=20.0))

    resp = client.get("/api/transactions?search=widget")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["description"] == "Widget sale"


def test_list_transactions_date_filter(client: TestClient, db_session):
    svc = TransactionService()
    svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Early", amount=10.0))
    svc.create(db_session, TransactionCreate(date=date(2026, 6, 15), description="Middle", amount=20.0))

    resp = client.get("/api/transactions?from_date=2026-06-10")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["description"] == "Middle"


def test_get_transaction(client: TestClient, db_session):
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Get me", amount=50.0))

    resp = client.get(f"/api/transactions/{txn.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == txn.id
    assert data["description"] == "Get me"
    assert data["amount"] == 50.0


def test_get_transaction_not_found(client: TestClient, db_session):
    resp = client.get("/api/transactions/nonexistent-id")
    assert resp.status_code == 404
    data = resp.json()
    assert data["error"]["code"] == "NOT_FOUND"


def test_update_transaction(client: TestClient, db_session):
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Original", amount=100.0))

    resp = client.put(f"/api/transactions/{txn.id}", json={
        "description": "Updated",
        "amount": 200.0,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["description"] == "Updated"
    assert data["amount"] == 200.0
    assert data["date"] == "2026-06-01"  # unchanged


def test_update_transaction_partial(client: TestClient, db_session):
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(
        date=date(2026, 6, 1), description="Partial", amount=100.0, notes="Original notes",
    ))

    resp = client.put(f"/api/transactions/{txn.id}", json={
        "description": "Changed",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["description"] == "Changed"
    assert data["notes"] == "Original notes"  # unchanged
    assert data["amount"] == 100.0  # unchanged


def test_update_transaction_not_found(client: TestClient, db_session):
    resp = client.put("/api/transactions/nonexistent", json={"description": "Nope"})
    assert resp.status_code == 404


def test_delete_transaction(client: TestClient, db_session):
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Delete", amount=50.0))

    resp = client.delete(f"/api/transactions/{txn.id}")
    assert resp.status_code == 204

    # Verify soft-deleted
    assert svc.get_by_id(db_session, txn.id) is None


def test_delete_transaction_not_found(client: TestClient, db_session):
    resp = client.delete("/api/transactions/nonexistent")
    assert resp.status_code == 404


def test_export_csv(client: TestClient, db_session):
    svc = TransactionService()
    svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="CSV test", amount=99.99))

    resp = client.get("/api/transactions/export")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "text/csv; charset=utf-8"
    assert "CSV test" in resp.text
    assert "99.99" in resp.text
