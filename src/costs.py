import pandas as pd
from typing import List, Dict, Any


def guess_frequency_from_line(line: str) -> str:
    l = line.lower()
    if any(x in l for x in ['monthly', 'per month', 'every month']):
        return 'monthly'
    if any(x in l for x in ['annual', 'per year', 'yearly']):
        return 'yearly'
    if any(x in l for x in ['per transaction', 'per txn', 'per transaction']):
        return 'per_txn'
    return 'unknown'


def annualize_fees(detected: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for d in detected:
        line = d.get('line', '')
        typ = d.get('type')
        val = d.get('value')
        freq = guess_frequency_from_line(line)
        annual_cost = None
        if typ == 'amount' and val is not None:
            if freq == 'monthly':
                annual_cost = val * 12
            elif freq == 'yearly':
                annual_cost = val
            elif freq == 'per_txn':
                # unknown transaction count — leave as NaN
                annual_cost = None
            else:
                # assume one-off
                annual_cost = val
        elif typ == 'percent' and val is not None:
            # percent-based fees need context (e.g., amount of txns); mark as NaN for now
            annual_cost = None

        rows.append({
            'line': line,
            'type': typ,
            'value': val,
            'frequency': freq,
            'annual_cost_estimate': annual_cost
        })

    df = pd.DataFrame(rows)
    # fill numeric NaNs consistently
    if 'annual_cost_estimate' in df.columns:
        df['annual_cost_estimate'] = pd.to_numeric(df['annual_cost_estimate'], errors='coerce')
    return df
