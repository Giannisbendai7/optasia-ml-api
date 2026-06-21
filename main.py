from fastapi import FastAPI, Depends
from typing import List
from sqlalchemy.orm import Session
from logger import logger



from schemas import RequestBody
from feature_engineering import generate_features

from database import engine, get_db
from models import Base, Transaction, Feature


logger.info("API started")

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
def create_features(payload: RequestBody, db: Session = Depends(get_db)):
    logger.info("Received /features request")

    # 1. Flatten loans
    all_loans = []

    for customer in payload.data:
        all_loans.extend(customer.loans)

    # 2. Generate features
    features = generate_features(all_loans)
    logger.info("Features generated")

    # 3. Save transactions
    logger.info("Saving transactions")

    for customer in payload.data:
        for loan in customer.loans:
            db.add(Transaction(
                customer_id=customer.customer_ID,
                loan_date=loan.loan_date,
                amount=loan.amount,
                fee=loan.fee,
                loan_status=loan.loan_status,
                term=loan.term,
                annual_income=loan.annual_income
            ))

    db.commit()

    # 4. Save features (per first customer)
    logger.info("Saving features")

    db.add(Feature(
        customer_id=payload.data[0].customer_ID,
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

