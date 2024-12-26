from celery import Celery
from app import models, database
from sqlalchemy.orm import Session
import heapq

# Initialize Celery with Redis as the broker
celery = Celery(__name__, broker="redis://localhost:6379/0")

# Celery configuration to enable retrying the connection on startup
celery.conf.update(
    result_backend="redis://localhost:6379/0",
    broker_connection_retry_on_startup=True,  # Use this setting to enable connection retries on startup
)

@celery.task
def update_statistics():
    db = database.SessionLocal()
    transactions = db.query(models.Transaction).all()
    total_transactions = len(transactions)
    total_amount = sum([t.amount for t in transactions])
    average_transaction_amount = total_amount / total_transactions if total_transactions > 0 else 0

    # Find top 3 largest transactions using heap
    top_transactions = heapq.nlargest(3, transactions, key=lambda t: t.amount)

    # Save stats or cache them (This is a simplified version)
    return {
        "total_transactions": total_transactions,
        "average_transaction_amount": average_transaction_amount,
        "top_transactions": [{"transaction_id": t.transaction_id, "amount": t.amount} for t in top_transactions]
    }

@celery.task
def clear_statistics():
    # Placeholder function to clear statistics
    pass

def get_statistics():
    db = database.SessionLocal()
    # Query to get all transactions
    transactions = db.query(models.Transaction).all()

    # Calculate total number of transactions
    total_transactions = len(transactions)

    # Calculate the total amount and average transaction amount
    total_amount = sum(t.amount for t in transactions)
    average_transaction_amount = total_amount / total_transactions if total_transactions > 0 else 0

    # Find top 3 largest transactions using heap
    top_transactions = heapq.nlargest(3, transactions, key=lambda t: t.amount)

    # Prepare response data
    statistics = {
        "total_transactions": total_transactions,
        "average_transaction_amount": average_transaction_amount,
        "top_transactions": [
            {"transaction_id": t.transaction_id, "amount": t.amount} for t in top_transactions
        ]
    }

    return statistics
