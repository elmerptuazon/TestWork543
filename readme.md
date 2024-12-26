# Transaction Microservice

This microservice is designed to handle transactions, process statistics, and provide analysis using FastAPI, SQLAlchemy, Celery, Redis, and PostgreSQL.

## Running Locally

1. Install the dependencies to run locally ```pip install -r requirements.txt```

## Running via Docker

1. Run ```docker-compose up --build```

## Run test

1. Run ```docker-compose up --build```

2. Look for container name fastapi-web then open via terminal

3. Run ```pytest```

## Access Swagger API docs

1. After docker compose build go to browser and access http://localhost:8000/docs

2. In the lock icon use apikey, in this case use ```ApiKey kB4PnxuL9HV32Hf0oG8KbdyGcG39fNcU9Lw7wLkB6zIc```