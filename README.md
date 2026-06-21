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
📡 API Endpoints
Health Check

GET /health

Generate Features

POST /features

Request Body:

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
