from src.fee_detector import detect_fees_in_text


def test_detect_amounts_and_percents():
    text = """
    Payment convenience fee ₹49
    Foreign transaction markup 2.5%
    Processing Fee ₹99
    """
    fees = detect_fees_in_text(text)
    assert any(f['type'] == 'amount' and f['value'] == 49.0 for f in fees)
    assert any(f['type'] == 'percent' and f['value'] == 2.5 for f in fees)
    assert any(f['type'] == 'amount' and f['value'] == 99.0 for f in fees)
