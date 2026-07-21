"""Tests for limit API endpoints."""
from datetime import date

from fastapi.testclient import TestClient

from app.schemas.transaction import TransactionCreate
from app.services.transaction import TransactionService


def test_get_current_limit_no_transactions(client: TestClient, db_session):
    resp = client.get("/api/limits/current")
    assert resp.status_code == 200
    data = resp.json()
    assert data["limit"] == 10813.50
    assert data["used"] == 0.0
    assert data["remaining"] == 10813.50
    assert data["is_exceeded"] is False
    assert data["year"] is not None
    assert data["quarter"] is not None


def test_get_current_limit_with_usage(client: TestClient, db_session):
    svc = TransactionService()
    svc.create(db_session, TransactionCreate(date=date(2026, 7, 1), description="Sale 1", amount=1000.0))
    svc.create(db_session, TransactionCreate(date=date(2026, 7, 15), description="Sale 2", amount=500.50))

    resp = client.get("/api/limits/current")
    assert resp.status_code == 200
    data = resp.json()
    assert data["used"] == 1500.50
    assert data["remaining"] == 9313.0
    assert data["is_exceeded"] is False


def test_get_current_limit_exceeded(client: TestClient, db_session):
    svc = TransactionService()
    svc.create(db_session, TransactionCreate(date=date(2026, 7, 1), description="Big sale", amount=12000.0))

    resp = client.get("/api/limits/current")
    assert resp.status_code == 200
    data = resp.json()
    assert data["used"] == 12000.0
    assert data["remaining"] == 0.0
    assert data["is_exceeded"] is True
