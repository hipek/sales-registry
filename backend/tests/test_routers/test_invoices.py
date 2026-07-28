from datetime import date

from fastapi.testclient import TestClient

from app.schemas.transaction import TransactionCreate
from app.services.transaction import TransactionService


def test_get_invoice(client: TestClient, db_session):
    svc = TransactionService()
    txn = svc.create(
        db_session,
        TransactionCreate(
            date=date(2026, 6, 15),
            description="Filament PLA",
            amount=89.99,
        ),
    )

    resp = client.get(f"/api/invoices/{txn.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["invoice_number"] == "R/2026/001"
    assert data["issue_date"] == "2026-06-15"
    assert data["seller"]["name"] == "Jan Kowalski"
    assert data["items"][0]["description"] == "Filament PLA"
    assert data["items"][0]["total"] == 89.99
    assert data["total"] == 89.99


def test_get_invoice_not_found(client: TestClient, db_session):
    resp = client.get("/api/invoices/nonexistent")
    assert resp.status_code == 404


def test_get_invoice_twice_same_number(client: TestClient, db_session):
    svc = TransactionService()
    txn = svc.create(
        db_session,
        TransactionCreate(
            date=date(2026, 6, 1),
            description="Test",
            amount=10.0,
        ),
    )

    resp1 = client.get(f"/api/invoices/{txn.id}")
    resp2 = client.get(f"/api/invoices/{txn.id}")
    assert resp1.json()["invoice_number"] == resp2.json()["invoice_number"]


def test_download_invoice_pdf(client: TestClient, db_session):
    svc = TransactionService()
    txn = svc.create(
        db_session,
        TransactionCreate(
            date=date(2026, 6, 15),
            description="PDF test",
            amount=45.00,
        ),
    )

    resp = client.get(f"/api/invoices/{txn.id}/download")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.headers["content-disposition"] is not None
    assert ".pdf" in resp.headers["content-disposition"]


def test_download_invoice_pdf_content(client: TestClient, db_session):
    svc = TransactionService()
    txn = svc.create(
        db_session,
        TransactionCreate(
            date=date(2026, 7, 15),
            description="PDF content test",
            amount=123.45,
        ),
    )

    resp = client.get(f"/api/invoices/{txn.id}/download")
    assert resp.status_code == 200
    assert resp.content[:5] == b"%PDF-"
    assert len(resp.content) > 500


def test_download_invoice_not_found(client: TestClient, db_session):
    resp = client.get("/api/invoices/nonexistent/download")
    assert resp.status_code == 404
