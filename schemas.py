from pydantic import BaseModel, Field, field_validator
from typing import List, Literal


class Loan(BaseModel):
    loan_date: str

    amount: int = Field(..., ge=100, le=1000)

    fee: int = Field(..., ge=10, le=50)

    loan_status: Literal[0, 1]

    term: Literal["short", "long"]

    annual_income: int = Field(..., ge=100, le=10000000)


class CustomerLoans(BaseModel):
    customer_ID: str = Field(..., min_length=10, max_length=20)
    loans: List[Loan]

    @field_validator("customer_ID")
    @classmethod
    def validate_ascii(cls, value):
        if not value.isascii():
            raise ValueError("customer_ID must contain only ASCII characters")
        return value


class RequestBody(BaseModel):
    data: List[CustomerLoans]