import streamlit as st
from src.pdf_parser import extract_text_from_pdf_or_text
from src.fee_detector import detect_fees_in_text
from src.costs import annualize_fees
from src.summarizer import render_fee_nutrition_label, draft_complaint_email

st.set_page_config(page_title="FinFeeX — Hidden-Fees X-Ray", layout="centered")

st.title("FinFeeX — Hidden-Fees X-Ray (MVP)")
st.markdown("Upload a bank/credit card statement (PDF) or a plain .txt export to detect hidden fees.")

uploaded = st.file_uploader("Upload statement (PDF or .txt)", type=["pdf", "txt"])

if uploaded is not None:
    with st.spinner("Extracting text..."):
        text = extract_text_from_pdf_or_text(uploaded)

    st.subheader("Extracted text (first 800 chars)")
    st.text_area("extracted", value=(text[:800] + "..." if len(text) > 800 else text), height=200)

    st.subheader("Detected fees")
    fees = detect_fees_in_text(text)
    df = annualize_fees(fees)

    st.table(df)

    st.subheader("Fee Nutrition Label")
    label = render_fee_nutrition_label(df)
    st.markdown(label)

    st.subheader("Auto-draft complaint")
    email = draft_complaint_email(df)
    st.text_area("Email draft", value=email, height=200)
