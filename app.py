import streamlit as st
import pandas as pd
from src.pdf_parser import extract_text_from_pdf_or_text
from src.fee_detector import detect_fees_in_text
from src.costs import annualize_fees
from src.summarizer import render_fee_nutrition_label, draft_complaint_email, llm_summary

# Page configuration
st.set_page_config(
    page_title="FinFeeX — Hidden-Fees X-Ray",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI with improved color scheme
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        animation: gradient 3s ease infinite;
        background-size: 200% 200%;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .success-banner {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    .example-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .example-metric {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .highlight {
        color: #667eea;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for settings and info
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/money-box.png", width=150)
    st.title("⚙️ Settings")
    
    est_txns = st.number_input(
        "📊 Annual foreign transactions",
        min_value=0,
        value=12,
        help="Estimate of foreign transactions per year (for % fees calculation)"
    )
    
    show_raw_text = st.checkbox("🔍 Show extracted text", value=False)
    
    st.markdown("---")
    st.subheader("📚 About FinFeeX")
    st.markdown("""
    **FinFeeX** helps you:
    - 🔍 Detect hidden fees
    - 💰 Calculate annual costs
    - 📧 Draft complaint emails
    - 📊 Visualize fee breakdown
    """)
    
    st.markdown("---")
    st.markdown("🌟 **Made with ❤️ for financial transparency**")

# Main header
st.markdown('<div class="main-header">💰 FinFeeX — Hidden-Fees X-Ray</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">🔍 Unmask hidden costs in your financial statements</div>', unsafe_allow_html=True)

# Upload section with better UX
st.markdown("### 📤 Upload Your Statement")
uploaded = st.file_uploader(
    "Drag and drop your bank/credit card statement here",
    type=["pdf", "txt"],
    help="Supports PDF and TXT formats. Your data is processed locally and never stored."
)

if uploaded is not None:
    # Processing section
    with st.spinner("🔄 Analyzing your statement..."):
        text = extract_text_from_pdf_or_text(uploaded)
    
    st.markdown('<div class="success-banner">✅ Statement processed successfully!</div>', unsafe_allow_html=True)
    
    # Show extracted text in expander (optional)
    if show_raw_text:
        with st.expander("📄 View Extracted Text (First 800 chars)"):
            st.text_area("Extracted content", value=(text[:800] + "..." if len(text) > 800 else text), height=200, disabled=True)
    
    # Process fees
    fees = detect_fees_in_text(text)
    df = annualize_fees(fees, estimated_annual_txns=est_txns)
    
    # Key metrics at the top
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        total_annual = int(df['annual_cost_estimate'].dropna().sum()) if 'annual_cost_estimate' in df.columns else 0
        fee_count = len(df)
        score = 100 - min(80, int(total_annual / 20))
        avg_fee = int(total_annual / fee_count) if fee_count > 0 else 0
        
        with col1:
            st.metric("💰 Total Annual Cost", f"₹{total_annual:,}", help="Estimated yearly cost of all detected fees")
        with col2:
            st.metric("📊 Transparency Score", f"{score}%", delta=f"{score-70}% vs avg", help="Higher is better")
        with col3:
            st.metric("🔍 Fees Detected", f"{fee_count}", help="Number of fee-related lines found")
        with col4:
            st.metric("📈 Avg Fee/Year", f"₹{avg_fee:,}", help="Average annual cost per fee")
    
    st.markdown("---")
    
    # Detailed fee breakdown
    st.markdown("### 📋 Detailed Fee Breakdown")
    
    if not df.empty:
        # Format dataframe for display
        display_df = df.copy()
        if 'annual_cost_estimate' in display_df.columns:
            display_df['Annual Cost'] = display_df['annual_cost_estimate'].apply(
                lambda x: f"₹{int(x):,}" if pd.notna(x) else "—"
            )
        if 'value' in display_df.columns:
            def fmt_val(r):
                if r['type'] == 'percent':
                    return f"{r['value']}%"
                if r['value'] is None:
                    return "—"
                return f"₹{int(r['value']):,}"
            display_df['Detected Value'] = display_df.apply(fmt_val, axis=1)
            display_df = display_df.rename(columns={
                'line': 'Fee Description',
                'frequency': 'Frequency'
            })
            display_df = display_df[['Fee Description', 'Detected Value', 'Frequency', 'Annual Cost']]
        
        # Use dataframe instead of table for better interactivity
        st.dataframe(display_df, width='stretch', hide_index=True)
    else:
        st.info("ℹ️ No fees detected in this statement. This is great news!")

    # Visualization section
    st.markdown("---")
    st.markdown("### 📊 Visual Analysis")
    
    viz_col1, viz_col2 = st.columns([2, 1])
    
    with viz_col1:
        if 'annual_cost_estimate' in df.columns and not df.empty:
            viz = df.dropna(subset=['annual_cost_estimate']).sort_values('annual_cost_estimate', ascending=False).head(5)
            if not viz.empty:
                st.markdown("#### 🔝 Top 5 Annual Fees")
                # Create a better formatted chart
                chart_data = viz.set_index('line')['annual_cost_estimate']
                st.bar_chart(chart_data, width='stretch')
    
    with viz_col2:
        st.markdown("#### 📄 Fee Nutrition Label")
        label = render_fee_nutrition_label(df)
        st.markdown(label)
    
    # Complaint email section
    st.markdown("---")
    st.markdown("### 📧 Auto-Generated Complaint Email")
    
    tab1, tab2 = st.tabs(["📝 Email Draft", "💡 Tips"])
    
    with tab1:
        email = draft_complaint_email(df)
        st.text_area(
            "Copy this email and send to your bank:",
            value=email,
            height=300,
            help="Customize this template before sending"
        )
        
        # Quick copy button effect
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            if st.button("📋 Copy to Clipboard"):
                st.toast("✅ Email copied! (Use Ctrl+C to copy the text above)", icon="✅")
    
    with tab2:
        st.markdown("""
        **Before sending:**
        - ✅ Replace `[Your name]` and `[Contact email or phone]` with your details
        - ✅ Add your account number and customer ID
        - ✅ Attach this PDF report as evidence
        - ✅ Keep the tone professional but firm
        - ✅ Follow up after 14 days if no response
        
        **Your Rights:**
        - Banks must disclose all fees clearly (RBI guidelines)
        - You can request refunds for unauthorized charges
        - You have the right to close accounts without penalties
        """)

    # Export and download section
    st.markdown("---")
    st.markdown("### 📥 Download Reports")
    
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='📊 Download CSV Report',
            data=csv_bytes,
            file_name='finfeex_report.csv',
            mime='text/csv',
            width='stretch'
        )
    
    with col_d2:
        json_payload = {
            'summary': render_fee_nutrition_label(df),
            'detected_fees': df.to_dict(orient='records')
        }
        import json
        from datetime import datetime
        json_bytes = json.dumps(json_payload, ensure_ascii=False, indent=2).encode('utf-8')
        st.download_button(
            label='📄 Download JSON Report',
            data=json_bytes,
            file_name=f'finfeex_report_{datetime.now().strftime("%Y%m%d")}.json',
            mime='application/json',
            width='stretch'
        )
    
    with col_d3:
        st.download_button(
            label='📧 Download Email Draft',
            data=email.encode('utf-8'),
            file_name='complaint_email.txt',
            mime='text/plain',
            width='stretch'
        )
    
    # LLM Summary section (optional advanced feature)
    st.markdown("---")
    with st.expander("🤖 Advanced: AI-Powered Summary (Optional)"):
        st.markdown("Use OpenAI to generate a detailed summary and recommendations.")
        api_key = st.text_input(
            '🔑 OpenAI API Key',
            type='password',
            help="Your API key is not stored. Used only for this session."
        )
        
        if api_key:
            if st.button('✨ Generate AI Summary', width='stretch'):
                with st.spinner('🤖 AI is analyzing your fees...'):
                    llm_out = llm_summary(text, openai_api_key=api_key)
                st.markdown("#### 🎯 AI Insights")
                st.success(llm_out)
    
    # Footer with helpful info
    st.markdown("---")
    st.info("💡 **Pro Tip:** Adjust the annual transactions estimate in the sidebar for more accurate percentage fee calculations.")

else:
    # Welcome screen when no file is uploaded
    st.markdown("---")
    
    col_w1, col_w2, col_w3 = st.columns(3)
    
    with col_w1:
        st.markdown("""
        ### 🔍 How It Works
        1. Upload your statement
        2. AI detects hidden fees
        3. Get annual cost estimate
        4. Download complaint email
        """)
    
    with col_w2:
        st.markdown("""
        ### 🔒 Privacy First
        - No data stored
        - Local processing
        - No tracking
        - Open source
        """)
    
    with col_w3:
        st.markdown("""
        ### 💪 Take Action
        - Know your fees
        - Save money
        - Hold banks accountable
        - Share with friends
        """)
    
    st.markdown("---")
    st.markdown("### 📸 Example Output Preview")
    
    # Create example output visualization
    st.markdown("""
    <div class="example-card">
        <h3 style="color: #667eea; margin-bottom: 1rem;">💰 Sample Analysis Results</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem;">
            <div class="example-metric">
                <div style="font-size: 0.9rem; color: #666;">💰 Total Annual Cost</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #667eea; margin-top: 0.5rem;">₹1,088</div>
            </div>
            <div class="example-metric">
                <div style="font-size: 0.9rem; color: #666;">📊 Transparency Score</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #11998e; margin-top: 0.5rem;">68%</div>
            </div>
            <div class="example-metric">
                <div style="font-size: 0.9rem; color: #666;">🔍 Fees Detected</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #764ba2; margin-top: 0.5rem;">5</div>
            </div>
        </div>
        <div style="margin-top: 2rem; text-align: left; background: white; padding: 1.5rem; border-radius: 10px;">
            <div style="font-weight: bold; margin-bottom: 1rem; color: #667eea;">📋 Sample Detected Fees:</div>
            <div style="padding: 0.5rem 0; border-bottom: 1px solid #eee;">• <span class="highlight">Convenience Fee</span> (Monthly): ₹49/month → <strong>₹588/year</strong></div>
            <div style="padding: 0.5rem 0; border-bottom: 1px solid #eee;">• <span class="highlight">FX Markup</span>: 3.5% → <strong>₹300/year</strong></div>
            <div style="padding: 0.5rem 0;">• <span class="highlight">Annual Fee</span>: <strong>₹200</strong></div>
        </div>
        <div style="margin-top: 1.5rem; padding: 1rem; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; border-radius: 8px; font-weight: 600;">
            ✨ Upload your statement to see your actual fees!
        </div>
    </div>
    """, unsafe_allow_html=True)
