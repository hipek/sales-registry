from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models.transaction import Base
from app.schemas.transaction import TransactionCreate
from app.services.invoice import InvoiceService
from app.services.transaction import TransactionService


def _create_engine(tmp_path: Path) -> object:
    return create_engine(f"sqlite:///{tmp_path / 'db.sqlite'}", connect_args={"check_same_thread": False})


def _make_sessions(engine, count: int) -> list[Session]:
    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return [TestingSession() for _ in range(count)]


def _create_invoice(db: Session, transaction_id: str, inv_svc: InvoiceService):
    return inv_svc.get_or_create_invoice(
        db,
        transaction_id,
        type(
            "Settings",
            (),
            {
                "receipt_prefix": "R",
                "seller_name": "Test",
                "seller_address": "Test St",
                "seller_nip": "1234567890",
                "receipt_unit": "szt.",
            },
        )(),
    )


def _create_txn(db: Session, description: str):
    svc = TransactionService()
    return svc.create(
        db,
        TransactionCreate(
            date=date(2026, 6, 15),
            description=description,
            amount=100.0,
        ),
    )


def _create_txns(db: Session, count: int):
    return [_create_txn(db, f"Concurrent txn {idx}") for idx in range(count)]


def test_concurrent_invoice_creation(tmp_path: Path):
    """Test that concurrent invoice creation produces unique invoice numbers."""
    engine = _create_engine(tmp_path)
    Base.metadata.create_all(bind=engine)
    init_db = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    inv_svc = InvoiceService()
    sessions = _make_sessions(engine, 2)

    try:
        txns = _create_txns(init_db, 2)
        transaction_ids = [txn.id for txn in txns]

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(
                executor.map(
                    lambda pair: _create_invoice(pair[0], pair[1], inv_svc),
                    zip(sessions, transaction_ids, strict=True),
                )
            )

        # Verify counter was incremented correctly
        from app.models.counter import Counter

        counter = init_db.query(Counter).filter(Counter.id == "receipt-2026").first()
        assert counter is not None
        assert counter.value == 2

    finally:
        init_db.close()
        for session in sessions:
            session.close()
        engine.dispose()

    assert len(results) == 2
    assert sorted(result.invoice_number for result in results) == ["R/2026/001", "R/2026/002"]


def test_concurrent_invoice_creation_many(tmp_path: Path):
    """Test that many concurrent invoice creations produce unique invoice numbers."""
    engine = _create_engine(tmp_path)
    Base.metadata.create_all(bind=engine)
    init_db = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    inv_svc = InvoiceService()
    num_threads = 10
    sessions = _make_sessions(engine, num_threads)

    try:
        txns = _create_txns(init_db, num_threads)
        transaction_ids = [txn.id for txn in txns]

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = list(
                executor.map(
                    lambda pair: _create_invoice(pair[0], pair[1], inv_svc),
                    zip(sessions, transaction_ids, strict=True),
                )
            )

        # Verify counter value
        from app.models.counter import Counter

        counter = init_db.query(Counter).filter(Counter.id == "receipt-2026").first()
        assert counter is not None
        assert counter.value == num_threads

    finally:
        init_db.close()
        for session in sessions:
            session.close()
        engine.dispose()

    assert len(results) == num_threads
    invoice_numbers = [r.invoice_number for r in results]
    assert sorted(invoice_numbers) == [f"R/2026/{idx:03d}" for idx in range(1, num_threads + 1)]
