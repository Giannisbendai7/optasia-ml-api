from fastapi import FastAPI, Depends
from typing import List
from sqlalchemy.orm import Session

import logging

from schemas import Loan
from feature_engineering import generate_features

from database import engine, get_db
from models import Base, Transaction, Feature

# -----------------------
# LOGGING SETUP
# -----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------
# APP INIT
# -----------------------
app = FastAPI()

# -----------------------
# DB INIT (for assignment)
# -----------------------
Base.metadata.create_all(bind=engine)


# -----------------------
# HEALTH CHECK
# -----------------------
@app.get("/health")
def health():
    return {"status": "UP"}


# -----------------------
# CREATE FEATURES
# -----------------------
@app.post("/features")
def create_features(
    loans: List[Loan],
    db: Session = Depends(get_db)
):
    logger.info("Received /features request")

    # 1. Generate features
    features = generate_features(loans)
    logger.info("Features generated")

    # 2. Save raw transactions
    logger.info("Saving transactions")
    for loan in loans:
        db.add(Transaction(
            customer_id=loan.customer_ID,
            loan_date=loan.loan_date,
            amount=loan.amount,
            fee=loan.fee,
            loan_status=loan.loan_status,
            term=loan.term,
            annual_income=loan.annual_income
        ))

    db.commit()

    # 3. Save features
    logger.info("Saving features")
    db.add(Feature(
        customer_id=loans[0].customer_ID,
        total_loans=features["total_loans"],
        total_amount=features["total_amount"],
        total_fees=features["total_fees"],
        avg_amount=features["avg_amount"],
        max_amount=features["max_amount"],
        default_rate=features["default_rate"],
        income_to_loan_ratio=features["income_to_loan_ratio"]
    ))

    db.commit()

    logger.info("Process completed")

    return {"features": features}


# -----------------------
# GET TRANSACTIONS
# -----------------------
@app.get("/transactions/{customer_id}")
def get_transactions(
    customer_id: str,
    db: Session = Depends(get_db)
):
    return db.query(Transaction).filter(
        Transaction.customer_id == customer_id
    ).all()


# -----------------------
# GET FEATURES
# -----------------------
@app.get("/features/{customer_id}")
def get_features(
    customer_id: str,
    db: Session = Depends(get_db)
):
    return db.query(Feature).filter(
        Feature.customer_id == customer_id
    ).all()


# -----------------------
# DELETE TRANSACTIONS
# -----------------------
@app.delete("/transactions/{customer_id}")
def delete_transactions(
    customer_id: str,
    db: Session = Depends(get_db)
):
    logger.info(f"Deleting transactions for {customer_id}")

    deleted = db.query(Transaction).filter(
        Transaction.customer_id == customer_id
    ).delete()

    db.commit()

    return {
        "message": f"Transactions deleted",
        "deleted_rows": deleted
    }


# -----------------------
# DELETE FEATURES
# -----------------------
@app.delete("/features/{customer_id}")
def delete_features(
    customer_id: str,
    db: Session = Depends(get_db)
):
    logger.info(f"Deleting features for {customer_id}")

    deleted = db.query(Feature).filter(
        Feature.customer_id == customer_id
    ).delete()

    db.commit()

    return {
        "message": f"Features deleted",
        "deleted_rows": deleted
    }

