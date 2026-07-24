from concurrent.futures import ThreadPoolExecutor
from datetime import date

from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.invoice import InvoiceService
from app.services.transaction import TransactionService


def test_concurrent_invoice_creation(db_session: Session):
    """Test that concurrent invoice creation produces unique invoice numbers."""
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(
        date=date(2026, 6, 15),
        description="Concurrent test",
        amount=100.0,
    ))

    inv_svc = InvoiceService()

    def create_invoice():
        return inv_svc.get_or_create_invoice(
            db_session, txn,
            type('Settings', (), {
                'receipt_prefix': 'R',
                'seller_name': 'Test',
                'seller_address': 'Test St',
                'seller_nip': '1234567890',
                'receipt_unit': 'szt.',
            })()
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(create_invoice, range(2)))

    assert len(results) == 2
    assert results[0].invoice_number != results[1].invoice_number

    # Verify counter was incremented correctly
    from app.models.counter import Counter
    counter = db_session.query(Counter).filter(Counter.id == "receipt-2026").first()
    assert counter is not None
    assert counter.value == 2


def test_concurrent_invoice_creation_many(db_session: Session):
    """Test that many concurrent invoice creations produce unique invoice numbers."""
    svc = TransactionService()
    txn = svc.create(db_session, TransactionCreate(
        date=date(2026, 6, 15),
        description="Concurrent test many",
        amount=100.0,
    ))

    inv_svc = InvoiceService()

    def create_invoice():
        return inv_svc.get_or_create_invoice(
            db_session, txn,
            type('Settings', (), {
                'receipt_prefix': 'R',
                'seller_name': 'Test',
                'seller_address': 'Test St',
                'seller_nip': '1234567890',
                'receipt_unit': 'szt.',
            })()
        )

    num_threads = 10
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(create_invoice, range(num_threads)))

    assert len(results) == num_threads
    invoice_numbers = [r.invoice_number for r in results]
    assert len(invoice_numbers) == len(set(invoice_numbers))  # All unique

    # Verify counter value
    from app.models.counter import Counter
    counter = db_session.query(Counter).filter(Counter.id == "receipt-2026").first()
    assert counter is not None
    assert counter.value == num_threads
