from pydantic import BaseModel, Field
from typing import Literal


class Loan(BaseModel):
    customer_ID: str = Field(..., min_length=10, max_length=20)

    loan_date: str

    amount: int = Field(..., ge=100, le=1000)
    fee: int = Field(..., ge=10, le=50)

    loan_status: int = Field(..., ge=0, le=1)

    term: Literal["short", "long"]

    annual_income: int = Field(..., ge=100, le=10000000) 