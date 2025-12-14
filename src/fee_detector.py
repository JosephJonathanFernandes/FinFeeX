import re
from typing import List, Dict, Any

AMOUNT_RE = re.compile(r"(?P<currency>[₹$€£])?\s?(?P<amount>\d{1,3}(?:[\,\d]*)(?:\.\d+)?)")
PERCENT_RE = re.compile(r"(?P<percent>\d+(?:\.\d+)?)\s?%")

FEE_KEYWORDS = [
    "fee", "convenience", "processing", "service charge", "service", "markup",
    "foreign transaction", "fx", "txn charge", "transaction fee", "charge"
]


def detect_fees_in_text(text: str) -> List[Dict[str, Any]]:
    """Return a list of fee candidates with extracted amount/percent and context line."""
    candidates = []
    for line in text.splitlines():
        l = line.lower()
        if any(k in l for k in FEE_KEYWORDS):
            # find percent
            p = PERCENT_RE.search(l)
            amt = None
            if p:
                candidates.append({"line": line.strip(), "type": "percent", "value": float(p.group('percent'))})
                continue

            m = AMOUNT_RE.search(line)
            if m:
                raw = m.group('amount').replace(',', '')
                try:
                    amt = float(raw)
                except Exception:
                    amt = None

            candidates.append({"line": line.strip(), "type": "amount" if amt is not None else "unknown", "value": amt, "currency": m.group('currency') if m else None})

    return candidates