from typing import Optional
import pandas as pd


def render_fee_nutrition_label(df: pd.DataFrame) -> str:
    total_hidden = df['annual_cost_estimate'].dropna().sum() if 'annual_cost_estimate' in df.columns else 0
    count = len(df)
    score = max(20, 100 - int(total_hidden / 10)) if total_hidden else 100

    md = f"**Transparency Score:** {score}%  \n\n"
    md += f"**Total Annual Hidden Cost (estimate):** ₹{int(total_hidden) if total_hidden else 0}  \n\n"
    md += f"**Detected fee lines:** {count}"
    return md


def draft_complaint_email(df: pd.DataFrame, recipient_name: Optional[str]='Support') -> str:
    lines = df['line'].tolist() if 'line' in df.columns else []
    top = '\n'.join(lines[:5])
    email = f"Dear {recipient_name},\n\nI have reviewed my recent statements and found recurring fees that are unclear or undisclosed:\n\n{top}\n\nPlease clarify the purpose of these fees and provide a refund if they were charged in error. I would like a written response within 14 days.\n\nThanks,\n[Your name]"
    return email
