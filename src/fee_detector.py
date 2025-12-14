import re
from typing import List, Dict, Any

AMOUNT_RE = re.compile(r"(?P<currency>[₹$€£])?\s?(?P<amount>\d{1,3}(?:[\,\d]*)(?:\.\d+)?)")
PERCENT_RE = re.compile(r"(?P<percent>\d+(?:\.\d+)?)\s?%")

FEE_KEYWORDS = [
    "fee", "convenience", "processing", "service charge", "service", "markup",
    "foreign transaction", "fx", "txn charge", "transaction fee", "charge",
    "annual", "renewal", "membership", "maintenance", "late payment", "penalty",
    "overdraft", "minimum balance", "atm", "cash withdrawal", "sms", "alert",
    "card replacement", "statement", "courier", "cheque", "swipe", "interchange",
    "fuel surcharge", "reward redemption", "lounge access", "insurance"
]


def categorize_fee(line: str) -> str:
    """Categorize fee based on keywords in the line."""
    line_lower = line.lower()
    
    if any(k in line_lower for k in ["foreign", "fx", "currency"]):
        return "Foreign Exchange"
    elif any(k in line_lower for k in ["annual", "renewal", "membership"]):
        return "Annual/Renewal"
    elif any(k in line_lower for k in ["maintenance", "minimum balance"]):
        return "Account Maintenance"
    elif any(k in line_lower for k in ["late payment", "penalty", "overdraft"]):
        return "Penalties"
    elif any(k in line_lower for k in ["atm", "cash withdrawal"]):
        return "ATM/Withdrawal"
    elif any(k in line_lower for k in ["convenience", "processing", "transaction"]):
        return "Transaction Fees"
    elif any(k in line_lower for k in ["sms", "alert", "statement"]):
        return "Communication"
    else:
        return "Other Fees"


def detect_fees_in_text(text: str) -> List[Dict[str, Any]]:
    """Return a list of fee candidates with extracted amount/percent and context line."""
    candidates = []
    for line in text.splitlines():
        l = line.lower()
        if any(k in l for k in FEE_KEYWORDS):
            # find percent
            p = PERCENT_RE.search(l)
            amt = None
            category = categorize_fee(line)
            
            if p:
                candidates.append({"line": line.strip(), "type": "percent", "value": float(p.group('percent')), "category": category})
                continue

            m = AMOUNT_RE.search(line)
            if m:
                raw = m.group('amount').replace(',', '')
                try:
                    amt = float(raw)
                except Exception:
                    amt = None

            candidates.append({"line": line.strip(), "type": "amount" if amt is not None else "unknown", "value": amt, "currency": m.group('currency') if m else None, "category": category})

    return candidates