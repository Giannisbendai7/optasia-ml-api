from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(String)
    loan_date = Column(String)

    amount = Column(Integer)
    fee = Column(Integer)

    loan_status = Column(Integer)
    term = Column(String)

    annual_income = Column(Integer)


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(String)

    total_loans = Column(Integer)
    total_amount = Column(Float)
    total_fees = Column(Float)

    avg_amount = Column(Float)
    max_amount = Column(Float)

    default_rate = Column(Float)
    income_to_loan_ratio = Column(Float)