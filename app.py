import streamlit as st
import pandas as pd
from src.pdf_parser import extract_text_from_pdf_or_text
from src.fee_detector import detect_fees_in_text
from src.costs import annualize_fees
from src.summarizer import render_fee_nutrition_label, draft_complaint_email

st.set_page_config(page_title="FinFeeX — Hidden-Fees X-Ray", layout="wide")

st.title("FinFeeX — Hidden-Fees X-Ray (MVP)")
st.markdown("Upload a bank/credit card statement (PDF) or a plain .txt export to detect hidden fees.")

uploaded = st.file_uploader("Upload statement (PDF or .txt)", type=["pdf", "txt"] )

col1, col2 = st.columns([2, 1])

with col2:
    st.info("Tip: If your statement uses a different currency symbol, the detector will still pick amounts.")
    est_txns = st.number_input("Estimate of foreign transactions per year (for % fees)", min_value=0, value=12)

if uploaded is not None:
    with st.spinner("Extracting text..."):
        text = extract_text_from_pdf_or_text(uploaded)

    st.subheader("Extracted text (first 800 chars)")
    st.text_area("extracted", value=(text[:800] + "..." if len(text) > 800 else text), height=220)

    fees = detect_fees_in_text(text)
    df = annualize_fees(fees, estimated_annual_txns=est_txns)

    st.subheader("Detected fees")
    # format dataframe for display
    display_df = df.copy()
    if 'annual_cost_estimate' in display_df.columns:
        display_df['annual_cost_estimate'] = display_df['annual_cost_estimate'].apply(lambda x: f"₹{int(x)}" if pd.notna(x) else "—")
    if 'value' in display_df.columns:
        def fmt_val(r):
            if r['type'] == 'percent':
                return f"{r['value']}%"
            if r['value'] is None:
                return "—"
            return f"₹{int(r['value'])}"
        display_df['detected'] = display_df.apply(fmt_val, axis=1)
        display_df = display_df[['line', 'detected', 'frequency', 'annual_cost_estimate']]

    st.table(display_df)

    st.subheader("Fee Nutrition Label")
    label = render_fee_nutrition_label(df)
    st.markdown(label)

    st.subheader("Auto-draft complaint")
    email = draft_complaint_email(df)
    st.text_area("Email draft", value=email, height=220)
