import pytest
from src.fee_detector import categorize_fee


def test_categorize_foreign_exchange():
    assert categorize_fee("Foreign transaction fee 2.5%") == "Foreign Exchange"
    assert categorize_fee("FX markup charge") == "Foreign Exchange"
    assert categorize_fee("Currency conversion fee") == "Foreign Exchange"


def test_categorize_annual_fees():
    assert categorize_fee("Annual credit card fee") == "Annual/Renewal"
    assert categorize_fee("Membership renewal charge") == "Annual/Renewal"


def test_categorize_maintenance():
    assert categorize_fee("Monthly account maintenance") == "Account Maintenance"
    assert categorize_fee("Minimum balance fee") == "Account Maintenance"


def test_categorize_penalties():
    assert categorize_fee("Late payment penalty") == "Penalties"
    assert categorize_fee("Overdraft charge") == "Penalties"


def test_categorize_atm():
    assert categorize_fee("ATM withdrawal fee") == "ATM/Withdrawal"
    assert categorize_fee("Cash withdrawal charge") == "ATM/Withdrawal"


def test_categorize_transaction():
    assert categorize_fee("Convenience fee") == "Transaction Fees"
    assert categorize_fee("Processing charge") == "Transaction Fees"


def test_categorize_communication():
    assert categorize_fee("SMS alert service") == "Communication"
    assert categorize_fee("Statement courier fee") == "Communication"


def test_categorize_other():
    assert categorize_fee("Unknown mysterious fee") == "Other Fees"
