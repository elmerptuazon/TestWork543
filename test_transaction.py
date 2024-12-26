import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import Base, Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from alembic import command
from alembic.config import Config

TEST_DATABASE_URL = "postgresql://user:password@db/dbname"

# Setup the test database
engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="session")
def run_migrations():
    # Run alembic migrations before the tests start
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield
    # Clean up after all tests are done
    command.downgrade(alembic_cfg, "base")

@pytest.fixture(scope="function")
def db_session(run_migrations):
    # Create a new database session for each test
    db = SessionLocal()
    # Drop all tables and recreate them before each test (this ensures a clean state)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield db
    db.close()

@pytest.fixture
def override_get_db(db_session):
    # Override the dependency to use the test database session
    def _get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = _get_db

# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db

# Initialize the TestClient
client = TestClient(app)
headers = {
    'Accept': 'application/json',
    'Authorization': 'ApiKey kB4PnxuL9HV32Hf0oG8KbdyGcG39fNcU9Lw7wLkB6zIc'
}

def test_create_transaction():
    response = client.post("/transactions", json={
        "transaction_id": "10",
        "user_id": "test_user",
        "amount": 100.0,
        "currency": "USD",
        "timestamp": "2024-12-26T12:00:00Z"
    }, headers=headers)
    print(response.json())
    # Check for a successful response
    assert response.status_code == 201
    assert response.json().get('message') == 'Transaction received'

    # Check if the transaction is in the database
    db = SessionLocal()
    transaction = db.query(Transaction).filter(Transaction.transaction_id == "10").first()
    assert transaction is not None
    assert transaction.transaction_id == "10"
    assert transaction.user_id == "test_user"
    assert transaction.amount == 100.0
    db.close()


def test_delete_transaction():
    # Create a test transaction
    client.post("/transactions", json={
        "transaction_id": "1",
        "user_id": "test_user",
        "amount": 100.0,
        "currency": "USD",
        "timestamp": "2024-12-26T12:00:00Z"
    }, headers=headers)

    # Send a DELETE request to remove the transaction
    response = client.delete("/transactions", headers=headers)

    # Check for successful deletion
    assert response.status_code == 200
    assert response.json() == {"message": "All transactions deleted"}

    # Check if the transaction is removed from the database
    db = SessionLocal()
    transaction = db.query(Transaction).filter(Transaction.transaction_id == "1").first()
    assert transaction is None
    db.close()


def test_get_statistics():
    # Insert a few transactions
    client.post("/transactions", json={
        "transaction_id": "2",
        "user_id": "test_user_2",
        "amount": 150.0,
        "currency": "USD",
        "timestamp": "2024-12-26T13:00:00Z"
    }, headers=headers)

    # Send GET request for statistics
    response = client.get("/statistics", headers=headers)

    # Check the response status and values
    assert response.status_code == 200
    stats = response.json()
    assert "total_transactions" in stats
    assert "average_transaction_amount" in stats
    assert "top_transactions" in stats
    assert stats["total_transactions"] == 1
    assert stats["average_transaction_amount"] == 150.0
    assert stats["top_transactions"][0]['amount'] == 150.0
