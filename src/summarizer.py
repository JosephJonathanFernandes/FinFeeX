from typing import Optional
import pandas as pd


def render_fee_nutrition_label(df: pd.DataFrame) -> str:
    total_hidden = int(df['annual_cost_estimate'].dropna().sum()) if 'annual_cost_estimate' in df.columns else 0
    count = len(df)
    # Simple transparency heuristic: more money hidden -> lower score
    score = 100 - min(80, int(total_hidden / 20))

    md = f"**Transparency Score:** **{score}%**  \n\n"
    md += f"**Total Annual Hidden Cost (estimate):** **₹{total_hidden}**  \n\n"
    md += f"**Detected fee lines:** {count}  \n\n"

    # top offenders
    if 'annual_cost_estimate' in df.columns:
        top = df.dropna(subset=['annual_cost_estimate']).sort_values('annual_cost_estimate', ascending=False).head(3)
        if not top.empty:
            md += "**Top hidden fees (annual est.):**  \n"
            for _, r in top.iterrows():
                md += f"- {r['line']} — ₹{int(r['annual_cost_estimate'])}  \n"

    return md


def draft_complaint_email(df: pd.DataFrame, recipient_name: Optional[str] = 'Support') -> str:
    # Build friendly, actionable email referencing key detected fees
    top = df.dropna(subset=['annual_cost_estimate']).sort_values('annual_cost_estimate', ascending=False).head(5)
    fee_lines = '\n'.join([f"- {r['line']} (est. ₹{int(r['annual_cost_estimate'])})" for _, r in top.iterrows()]) if not top.empty else '\n'.join(df['line'].tolist()[:5])

    email = (
        f"Dear {recipient_name},\n\n"
        "I am writing regarding fees that appear on my account statements and which are unclear or not properly disclosed. "
        "Below are the items I found (please review and advise):\n\n"
        f"{fee_lines}\n\n"
        "Please provide a written explanation of the purpose of these fees, the legal basis for them, and confirm whether any of them can be refunded. "
        "If they are valid, please point me to the exact line in your T&Cs where these are clearly described. I would appreciate a response within 14 days.\n\n"
        "Thank you,\n[Your name]\n[Contact email or phone]"
    )

    return email


def llm_summary(text: str, openai_api_key: str = None) -> str:
    """Optional LLM-based summary using OpenAI API if api key provided.

    This function is intentionally simple and falls back to a short extractive summary if OpenAI isn't available.
    """
    try:
        if not openai_api_key:
            raise RuntimeError('No OpenAI key')
        import openai
        openai.api_key = openai_api_key
        prompt = (
            "You are a helpful assistant that summarizes detected fees from a bank statement.\n"
            "Given the extracted text, list top hidden fees and give a one-paragraph recommendation.\n\n" + text
        )
        resp = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{"role": "user", "content": prompt}], max_tokens=300)
        return resp['choices'][0]['message']['content'].strip()
    except Exception:
        # fallback: return the first 300 characters
        return (text[:300] + '...') if len(text) > 300 else text
