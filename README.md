# Optasia ML Feature Engineering API

## Overview
This project implements a FastAPI-based service for feature engineering on loan data.

It processes customer loan records, validates input data, stores transactions in SQLite, and generates aggregated customer features.

---

## Tech Stack
- Python 3.11
- FastAPI
- SQLite
- SQLAlchemy ORM
- Pydantic
- Docker
- Pytest
- Postman

---

## Features
- Input validation using Pydantic
- Feature engineering pipeline
- SQLite data persistence
- REST API with FastAPI
- Unit testing with pytest
- Dockerized deployment
- Logging support

---

## How to Run


### Install dependencies
pip install -r requirements.txt

---

### Run locally
uvicorn main:app --reload

---

### Run with Docker
docker build -t optasia-api .
docker run -p 8000:8000 optasia-api



-----

API Endpoints

Health Check

GET /health

Generate Features

POST /features

-------

Request Body Example
{
  "data": [
    {
      "customer_ID": "1234567890",
      "loans": [
        {
          "loan_date": "2024-01-01",
          "amount": 500,
          "fee": 20,
          "loan_status": 0,
          "term": "short",
          "annual_income": 5000
        }
      ]
    }
  ]
}

------

Get Transactions

GET /transactions/{customer_id}

Get Features

GET /features/{customer_id}

Delete Transactions

DELETE /transactions/{customer_id}

Delete Features

DELETE /features/{customer_id}

Testing

pytest


-------

## Monitoring

The API includes request-level monitoring through FastAPI middleware.

Captured metrics:
- Request latency
- CPU usage
- Memory usage

Metrics are logged through the application logging layer for observability and debugging.



## Validation Summary 

| Test Case | Field | Input Value | Expected | Result | Status |
|-----------|-------|-------------|----------|--------|--------|
| TC1 | amount | 500 | valid range (100–1000) | Accepted | PASS |
| TC2 | amount | 5000 | must be ≤ 1000 | Rejected (422) | PASS |
| TC3 | fee | 5 | must be ≥ 10 | Rejected (422) | PASS |
| TC4 | term | "medium" | only short/long | Rejected (422) | PASS |
| TC5 | loan_status | "0" | only 0 or 1 (int) | Rejected | PASS |
| TC6 | customer_ID | "123" | min length 10 | Rejected | PASS |
| TC7 | annual_income | 50000000 | max 10M | Rejected | PASS |



All validations are implemented using Pydantic constraints and were verified using Postman with both positive and negative test cases.
