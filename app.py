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

    # Small visualization: top 5 annual estimates
    if 'annual_cost_estimate' in df.columns:
        viz = df.dropna(subset=['annual_cost_estimate']).sort_values('annual_cost_estimate', ascending=False).head(5)
        if not viz.empty:
            st.subheader('Top estimated annual fees')
            viz_plot = viz.set_index('line')['annual_cost_estimate']
            st.bar_chart(viz_plot)

    st.markdown("---")
    st.subheader("Fee Nutrition Label")
    label = render_fee_nutrition_label(df)
    st.markdown(label)

    st.subheader("Auto-draft complaint")
    email = draft_complaint_email(df)
    st.text_area("Email draft", value=email, height=220)

    # Export buttons: CSV, JSON, and download email
    st.markdown("---")
    st.write('Download report & email')
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(label='Download CSV report', data=csv_bytes, file_name='finfeex_report.csv', mime='text/csv')

    json_payload = {
        'summary': render_fee_nutrition_label(df),
        'detected_fees': df.to_dict(orient='records')
    }
    import json, io, datetime
    json_bytes = json.dumps(json_payload, ensure_ascii=False, indent=2).encode('utf-8')
    st.download_button(label='Download JSON report', data=json_bytes, file_name='finfeex_report.json', mime='application/json')

    # Email download
    st.download_button(label='Download complaint email (.txt)', data=email.encode('utf-8'), file_name='complaint_email.txt', mime='text/plain')

    # Helpful tips and CTA
    st.info('You can copy the email text or download the report to share with your bank. For percent fees, adjust the "Estimate of foreign transactions per year" to refine the amount.')
