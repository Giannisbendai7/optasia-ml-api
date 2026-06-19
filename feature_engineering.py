from typing import List
from schemas import Loan

def generate_features(loans: List[Loan]):
    if not loans:
        return {}

    total_loans = len(loans)

    total_amount = sum(l.amount for l in loans)
    total_fees = sum(l.fee for l in loans)

    avg_amount = total_amount / total_loans

    max_amount = max(l.amount for l in loans)

    default_rate = sum(l.loan_status for l in loans) / total_loans

    income = loans[0].annual_income if loans else 0
    income_to_loan_ratio = income / total_amount if total_amount > 0 else 0

    return {
        "total_loans": total_loans,
        "total_amount": total_amount,
        "total_fees": total_fees,
        "avg_amount": avg_amount,
        "max_amount": max_amount,
        "default_rate": default_rate,
        "income_to_loan_ratio": income_to_loan_ratio
    }

