from datetime import date
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.counter import Counter
from app.services.invoice import InvoiceService
from app.services.transaction import TransactionService
from app.schemas.transaction import TransactionCreate


class FakeSettings:
    receipt_prefix = "R"
    seller_name = "Jan Kowalski"
    seller_address = "ul. Testowa 1, 00-001 Warszawa"
    seller_nip = "1234567890"
    receipt_unit = "szt."


def test_get_invoice_new(db_session: Session):
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(
        date=date(2026, 6, 15),
        description="Filament PLA",
        amount=89.99,
    ))

    inv_svc = InvoiceService()
    invoice = inv_svc.get_or_create_invoice(db_session, txn, FakeSettings())

    assert invoice.invoice_number == "R/2026/001"
    assert invoice.issue_date == "2026-06-15"
    assert invoice.seller.name == "Jan Kowalski"
    assert invoice.seller.nip == "1234567890"
    assert len(invoice.items) == 1
    assert invoice.items[0].description == "Filament PLA"
    assert invoice.items[0].total == 89.99
    assert invoice.total == 89.99

    counter = db_session.query(Counter).filter(Counter.id == "receipt-2026").first()
    assert counter is not None
    assert counter.value == 1


def test_get_invoice_increments_counter(db_session: Session):
    svc = TransactionService()
    txn1 = svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="First", amount=10.0))
    txn2 = svc.create(db_session, TransactionCreate(date=date(2026, 6, 2), description="Second", amount=20.0))

    inv_svc = InvoiceService()
    inv1 = inv_svc.get_or_create_invoice(db_session, txn1, FakeSettings())
    inv2 = inv_svc.get_or_create_invoice(db_session, txn2, FakeSettings())

    assert inv1.invoice_number == "R/2026/001"
    assert inv2.invoice_number == "R/2026/002"


def test_get_invoice_existing_number(db_session: Session):
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="Test", amount=50.0))

    inv_svc = InvoiceService()
    inv1 = inv_svc.get_or_create_invoice(db_session, txn, FakeSettings())
    assert inv1.invoice_number == "R/2026/001"

    inv2 = inv_svc.get_or_create_invoice(db_session, txn, FakeSettings())
    assert inv2.invoice_number == "R/2026/001"


def test_get_invoice_separate_years(db_session: Session):
    svc = TransactionService()
    txn_2025 = svc.create(db_session, TransactionCreate(date=date(2025, 12, 31), description="Old", amount=10.0))
    txn_2026 = svc.create(db_session, TransactionCreate(date=date(2026, 1, 1), description="New", amount=20.0))

    inv_svc = InvoiceService()
    inv_2025 = inv_svc.get_or_create_invoice(db_session, txn_2025, FakeSettings())
    inv_2026 = inv_svc.get_or_create_invoice(db_session, txn_2026, FakeSettings())

    assert inv_2025.invoice_number == "R/2025/001"
    assert inv_2026.invoice_number == "R/2026/001"


def test_get_invoice_no_nip(db_session: Session):
    class NoNipSettings:
        receipt_prefix = "R"
        seller_name = "Jan Kowalski"
        seller_address = "ul. Testowa 1"
        seller_nip = None
        receipt_unit = "szt."

    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(date=date(2026, 6, 1), description="No NIP", amount=10.0))

    inv_svc = InvoiceService()
    invoice = inv_svc.get_or_create_invoice(db_session, txn, NoNipSettings())

    assert invoice.seller.nip is None
