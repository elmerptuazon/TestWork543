from pydantic import BaseModel
from typing import List
from datetime import datetime

class Transaction(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    timestamp: datetime

class TransactionResponse(BaseModel):
    message: str
    task_id: str

class MessageResponse(BaseModel):
    message: str

class Statistics(BaseModel):
    total_transactions: int
    average_transaction_amount: float
    top_transactions: List[dict]
