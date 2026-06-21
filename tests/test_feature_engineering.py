from schemas import Loan
from feature_engineering import generate_features


def test_generate_features_single_loan():

    loans = [
        Loan(
            customer_ID="1234567890",
            loan_date="2024-01-01",
            amount=500,
            fee=20,
            loan_status=0,
            term="short",
            annual_income=5000
        )
    ]

    features = generate_features(loans)

    assert features["total_loans"] == 1
    assert features["total_amount"] == 500
    assert features["total_fees"] == 20
    assert features["default_rate"] == 0