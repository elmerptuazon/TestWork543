from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas, tasks, database
import os
from app.database import init_db


api_key_header = APIKeyHeader(name="Authorization")

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

# Database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define the API key validation
def api_key_auth(authorization: str = Depends(api_key_header)) -> str:
    if not authorization.startswith("ApiKey "):
        raise HTTPException(status_code=403, detail="Invalid API key format. Use 'ApiKey <your_api_key>'")
    
    api_key = authorization[len("ApiKey "):]
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return api_key

# POST /transactions endpoint
@app.post("/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
async def upload_transaction(transaction: schemas.Transaction, db: Session = Depends(get_db), api_key: str = Depends(api_key_auth)):
    # Check if transaction_id already exists
    if db.query(models.Transaction).filter(models.Transaction.transaction_id == transaction.transaction_id).first():
        raise HTTPException(status_code=400, detail="Transaction ID already exists")

    # Save the transaction
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    # Send task to update statistics
    task = tasks.update_statistics.apply_async()

    return {"message": "Transaction received", "task_id": task.id}

# DELETE /transactions endpoint
@app.delete("/transactions", response_model=schemas.MessageResponse)
async def delete_all_transactions(db: Session = Depends(get_db), api_key: str = Depends(api_key_auth)):
    db.query(models.Transaction).delete()
    db.commit()
    tasks.clear_statistics.apply_async()
    return {"message": "All transactions deleted"}

# GET /statistics endpoint
@app.get("/statistics", response_model=schemas.Statistics)
async def get_statistics(db: Session = Depends(get_db), api_key: str = Depends(api_key_auth)):
    stats = tasks.get_statistics()
    return stats
