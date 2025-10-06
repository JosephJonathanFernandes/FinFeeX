import pandas as pd
from typing import List, Dict, Any


def guess_frequency_from_line(line: str) -> str:
    l = line.lower()
    if any(x in l for x in ['monthly', 'per month', 'every month', 'monthly)']):
        return 'monthly'
    if any(x in l for x in ['annual', 'per year', 'yearly', 'annually']):
        return 'yearly'
    if any(x in l for x in ['per transaction', 'per txn', 'per transaction', 'per txn)']):
        return 'per_txn'
    return 'unknown'


def annualize_fees(detected: List[Dict[str, Any]], estimated_annual_txns: int = 0, assumed_txn_value: float = 100.0) -> pd.DataFrame:
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
                if estimated_annual_txns:
                    annual_cost = val * estimated_annual_txns
                else:
                    annual_cost = None
            else:
                # assume one-off
                annual_cost = val
        elif typ == 'percent' and val is not None:
            # Estimate percent-based annual cost: assume estimated_annual_txns and an assumed_txn_value
            if estimated_annual_txns:
                # val is a percent, apply to total yearly txn volume
                yearly_volume = estimated_annual_txns * assumed_txn_value
                annual_cost = (val / 100.0) * yearly_volume
            else:
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
