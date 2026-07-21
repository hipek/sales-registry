import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.models.transaction import Base
from app.database import get_db
from app.main import app


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def _test_settings():
    from app.config import settings

    original_name = settings.seller_name
    original_address = settings.seller_address
    original_nip = settings.seller_nip
    original_prefix = settings.receipt_prefix

    settings.seller_name = "Jan Kowalski"
    settings.seller_address = "ul. Testowa 1, 00-001 Warszawa"
    settings.seller_nip = "1234567890"
    settings.receipt_prefix = "R"

    yield

    settings.seller_name = original_name
    settings.seller_address = original_address
    settings.seller_nip = original_nip
    settings.receipt_prefix = original_prefix


@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
