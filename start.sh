#!/bin/bash

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start the FastAPI app with uvicorn
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
