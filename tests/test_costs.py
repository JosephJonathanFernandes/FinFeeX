from src.costs import annualize_fees


def test_annualize_amounts_and_percents():
    detected = [
        {'line': 'Convenience fee ₹49 monthly', 'type': 'amount', 'value': 49.0},
        {'line': 'FX markup 2.5%', 'type': 'percent', 'value': 2.5},
        {'line': 'Processing Fee ₹99', 'type': 'amount', 'value': 99.0},
    ]

    df = annualize_fees(detected, estimated_annual_txns=12, assumed_txn_value=200)

    # convenience monthly -> 49*12
    conv = df[df['line'].str.contains('Convenience')].iloc[0]
    assert int(conv['annual_cost_estimate']) == 49 * 12

    # percent fee should be estimated: 2.5% of (12 * 200) = 60
    fx = df[df['line'].str.contains('FX')].iloc[0]
    assert int(round(fx['annual_cost_estimate'])) == 60

    proc = df[df['line'].str.contains('Processing')].iloc[0]
    assert int(proc['annual_cost_estimate']) == 99
