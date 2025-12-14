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

# Custom CSS for human-centered design
st.markdown("""
<style>
    /* Animated header with better visibility */
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
    
    /* More friendly subtitle */
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Welcoming success banner */
    .success-banner {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-weight: 600;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(17, 153, 142, 0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Friendly button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        cursor: pointer;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Better info boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #667eea;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Enhanced metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Better file uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 10%);
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 20%);
        transform: scale(1.01);
    }
    
    /* Progress indicator */
    .step-indicator {
        display: flex;
        justify-content: space-between;
        margin: 2rem 0;
        padding: 0 2rem;
    }
    .step {
        flex: 1;
        text-align: center;
        position: relative;
        padding: 1rem;
    }
    .step::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #e0e0e0;
        border: 3px solid #fff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .step.active::before {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .step.completed::before {
        background: #11998e;
        content: '✓';
        color: white;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Helpful tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
        color: #667eea;
        font-weight: 600;
    }
    
    /* Better card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    .info-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    
    /* Friendly example section */
    .example-card {
        background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 2px solid #e0e0e0;
    }
    .example-metric {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }
    .example-metric:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    .highlight {
        color: #667eea;
        font-weight: bold;
    }
    
    /* Smooth dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with human-centered design
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/money-box.png", width=120)
    
    st.markdown("### ⚙️ Quick Settings")
    
    with st.expander("📊 Configure Analysis", expanded=True):
        est_txns = st.number_input(
            "Annual foreign transactions",
            min_value=0,
            max_value=1000,
            value=12,
            help="💡 How many international transactions do you make per year? This helps calculate percentage-based FX fees."
        )
        
        show_raw_text = st.checkbox(
            "🔍 Show extracted text",
            value=False,
            help="View the raw text extracted from your statement"
        )
    
    st.markdown("---")
    
    # Progress tracker
    if 'fee_history' in st.session_state and len(st.session_state.fee_history) > 0:
        st.markdown("### 🎯 Your Progress")
        st.success(f"✅ {len(st.session_state.fee_history)} statement(s) analyzed")
        
        total_fees = sum(
            sum(f.get('annual_cost_estimate', 0) for f in entry['fees'])
            for entry in st.session_state.fee_history
        )
        st.metric("Total Fees Found", f"₹{int(total_fees):,}")
        
        if st.button("🔄 Analyze Another"):
            st.info("👆 Upload a new statement above")
    else:
        st.markdown("### 🚀 Getting Started")
        st.markdown("""
        **Quick Guide:**
        1. 📤 Upload your statement
        2. ⏳ Wait for analysis
        3. 📊 View your results
        4. 📧 Download reports
        
        **💡 Tip:** Start with the sample statement in `sample_data/` folder!
        """)
    
    st.markdown("---")
    
    with st.expander("📚 Learn More"):
        st.markdown("""
        **Why FinFeeX?**
        
        Banks hide fees in fine print. 
        We make them visible.
        
        - 🔒 100% Private
        - 🏗️ Open Source
        - 🔥 Always Free
        """)
    
    st.markdown("---")
    st.caption("🌟 Made with ❤️ for financial transparency")

# Main header with context
st.markdown('<div class="main-header">💰 FinFeeX — Hidden-Fees X-Ray</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">🕵️ Discover what your bank isn\'t telling you. Upload your statement and we\'ll find every hidden fee.</div>', unsafe_allow_html=True)

# Initialize session state for analytics
if 'fee_history' not in st.session_state:
    st.session_state.fee_history = []
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

# Progress indicator
if st.session_state.current_step > 1:
    st.markdown("""
    <div class="step-indicator">
        <div class="step completed">
            <div style="margin-top: 50px;">✅ Upload</div>
        </div>
        <div class="step {}">
            <div style="margin-top: 50px;">🔍 Analyze</div>
        </div>
        <div class="step {}">
            <div style="margin-top: 50px;">📊 Results</div>
        </div>
        <div class="step {}">
            <div style="margin-top: 50px;">📥 Download</div>
        </div>
    </div>
    """.format(
        "active" if st.session_state.current_step == 2 else "completed" if st.session_state.current_step > 2 else "",
        "active" if st.session_state.current_step == 3 else "completed" if st.session_state.current_step > 3 else "",
        "active" if st.session_state.current_step == 4 else ""
    ), unsafe_allow_html=True)

# Upload section with friendly guidance
st.markdown("")
st.markdown("### 👋 Let's Start Finding Your Hidden Fees")

col_intro1, col_intro2 = st.columns([3, 2])

with col_intro1:
    uploaded = st.file_uploader(
        "Drop your bank or credit card statement here",
        type=["pdf", "txt"],
        help="🔒 Your data stays private. We process everything locally and never store your information."
    )
    
with col_intro2:
    st.markdown("""
    <div class="info-card">
        <h4 style="color: #667eea; margin-top: 0;">💡 First Time?</h4>
        <p style="margin-bottom: 0; font-size: 0.9rem; color: #666;">
        Try our sample statement to see FinFeeX in action! Find it in:<br>
        <code>sample_data/sample_statement.txt</code>
        </p>
    </div>
    """, unsafe_allow_html=True)

if uploaded is not None:
    st.session_state.current_step = 2
    
    # Processing section with personality
    with st.spinner("🔍 Reading your statement... Looking for sneaky fees..."):
        text = extract_text_from_pdf_or_text(uploaded)
    
    st.session_state.current_step = 3
    st.markdown('<div class="success-banner">✅ Got it! We found your statement. Now let\'s see what they\'re charging you...</div>', unsafe_allow_html=True)
    
    # Show extracted text in expander (optional)
    if show_raw_text:
        with st.expander("📄 View Extracted Text (First 800 chars)"):
            st.text_area("Extracted content", value=(text[:800] + "..." if len(text) > 800 else text), height=200, disabled=True)
    
    # Process fees
    fees = detect_fees_in_text(text)
    df = annualize_fees(fees, estimated_annual_txns=est_txns)
    
    # Add to history for analytics (only if not already added)
    statement_name = uploaded.name
    if not any(h['name'] == statement_name for h in st.session_state.fee_history):
        from datetime import datetime
        st.session_state.fee_history.append({
            'name': statement_name,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'fees': df.to_dict('records')
        })
    
    # Show analytics link
    if len(st.session_state.fee_history) > 0:
        st.info(f"📊 {len(st.session_state.fee_history)} statement(s) tracked. Visit the **Analytics** page to see trends and comparisons!")
    
    # Key metrics with context
    if not df.empty:
        st.markdown("### 💡 Here's What We Found")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_annual = int(df['annual_cost_estimate'].dropna().sum()) if 'annual_cost_estimate' in df.columns else 0
        fee_count = len(df)
        score = 100 - min(80, int(total_annual / 20))
        avg_fee = int(total_annual / fee_count) if fee_count > 0 else 0
        
        with col1:
            st.metric(
                "💸 You're Paying",
                f"₹{total_annual:,}/year",
                help="This is what these fees cost you annually. Imagine what you could do with this money!"
            )
        
        with col2:
            delta_text = "Good" if score >= 80 else "Fair" if score >= 60 else "Poor"
            delta_color = "normal" if score >= 60 else "inverse"
            st.metric(
                "🎯 Transparency",
                f"{score}%",
                delta=delta_text,
                delta_color=delta_color,
                help="How transparent your bank is being. Higher is better!"
            )
        
        with col3:
            st.metric(
                "🔍 Fees Found",
                f"{fee_count}",
                help="Number of separate fees we detected. More fees = more places to save!"
            )
        
        with col4:
            st.metric(
                "📈 Average Fee",
                f"₹{avg_fee:,}/year",
                help="Average cost per fee annually"
            )
        
        # Emotional context based on total
        if total_annual > 2000:
            st.error("😱 **Wow, that's a lot!** You're paying over ₹2,000 in fees annually. Let's see if we can help you reduce this.")
        elif total_annual > 1000:
            st.warning("🤔 **That adds up!** Over ₹1,000 per year in fees. Worth reviewing if you can reduce these.")
        elif total_annual > 500:
            st.info("💡 **Moderate fees detected.** Not terrible, but there might be room for savings.")
        else:
            st.success("🎉 **Good news!** Your fees are relatively low. But every rupee saved is a rupee earned!")
    
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
                'frequency': 'Frequency',
                'category': 'Category'
            })
            # Include category in display
            cols = ['Category', 'Fee Description', 'Detected Value', 'Frequency', 'Annual Cost']
            display_df = display_df[[c for c in cols if c in display_df.columns]]
        
        # Use dataframe instead of table for better interactivity
        st.dataframe(display_df, width='stretch', hide_index=True)
    else:
        # Celebratory empty state
        st.markdown("""
        <div class="info-card" style="text-align: center; padding: 3rem;">
        <h2>🎉 Fantastic News!</h2>
        <p style="font-size: 1.2rem; margin-top: 1rem;">We didn't find any obvious fees in this statement.</p>
        <p style="color: #666; margin-top: 1rem;">This could mean:</p>
        <ul style="text-align: left; display: inline-block; margin-top: 1rem;">
        <li>✅ Your bank is being transparent</li>
        <li>✅ You have a zero-fee account</li>
        <li>✅ Fees might be on a different statement</li>
        </ul>
        <p style="margin-top: 2rem; color: #666;"><em>Try analyzing more statements to get the full picture!</em></p>
        </div>
        """, unsafe_allow_html=True)

    # Visualization section
    if not df.empty:
        st.markdown("---")
        st.markdown("### 📊 Visual Analysis")
        
        viz_col1, viz_col2 = st.columns([2, 1])
        
        with viz_col1:
            if 'annual_cost_estimate' in df.columns:
                viz = df.dropna(subset=['annual_cost_estimate']).sort_values('annual_cost_estimate', ascending=False).head(5)
                if not viz.empty:
                    st.markdown("#### 🔝 Top 5 Annual Fees")
                    # Create a better formatted chart
                    chart_data = viz.set_index('line')['annual_cost_estimate']
                    st.bar_chart(chart_data, width='stretch')
                    st.caption("💡 These are your biggest fee sources")
        
        with viz_col2:
            st.markdown("#### 📄 Fee Nutrition Label")
            label = render_fee_nutrition_label(df)
            st.markdown(label)
    
    # Complaint email section
    st.markdown("---")
    st.markdown("### 📧 Ready to Fight Back?")
    st.markdown("<p class='subtitle'>We've drafted a professional email for you. All you need to do is personalize it and hit send!</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Email Draft", "💡 Pro Tips"])
    
    with tab1:
        email = draft_complaint_email(df)
        st.markdown("**Your personalized complaint email:**")
        st.text_area(
            "Click inside to select all (Ctrl+A), then copy (Ctrl+C):",
            value=email,
            height=300,
            help="Feel free to modify this - make it yours!",
            label_visibility="collapsed"
        )
        
        # Helpful reminder
        st.info("💡 **Pro tip:** Don't forget to replace [Your name] and add your account details before sending!")
        
        # Quick copy button effect
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            if st.button("📋 Select All Text"):
                st.toast("✅ Text ready! Press Ctrl+A then Ctrl+C to copy", icon="📋")
    
    with tab2:
        st.markdown("""
        <div class="info-card">
        <h4>📝 Before You Send</h4>
        <ul>
        <li>✅ <strong>Personalize it:</strong> Replace [Your name] and contact details</li>
        <li>✅ <strong>Add specifics:</strong> Include your account number and customer ID</li>
        <li>✅ <strong>Attach proof:</strong> Download the CSV report below and attach it</li>
        <li>✅ <strong>Stay professional:</strong> Firm but polite gets better results</li>
        <li>✅ <strong>Follow through:</strong> Set a reminder to follow up in 14 days</li>
        </ul>
        </div>
        
        <div class="info-card" style="margin-top: 1rem;">
        <h4>⚖️ Know Your Rights</h4>
        <ul>
        <li>🛡️ Banks <strong>must</strong> disclose all fees clearly (RBI guidelines)</li>
        <li>💰 You <strong>can</strong> request refunds for unauthorized charges</li>
        <li>🚪 You <strong>have the right</strong> to close accounts without penalties</li>
        <li>📞 Contact RBI Banking Ombudsman if bank doesn't respond</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    # Export and download section
    st.markdown("---")
    st.markdown("### 📥 Take This With You")
    st.markdown("<p class='subtitle'>Save your analysis and use it as evidence when contacting your bank.</p>", unsafe_allow_html=True)
    
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label='📊 CSV Report',
            data=csv_bytes,
            file_name='finfeex_report.csv',
            mime='text/csv',
            help='Download as Excel/Sheets-friendly format',
            width='stretch'
        )
        st.caption("📈 Open in Excel")
    
    with col_d2:
        json_payload = {
            'summary': render_fee_nutrition_label(df),
            'detected_fees': df.to_dict(orient='records')
        }
        import json
        from datetime import datetime
        json_bytes = json.dumps(json_payload, ensure_ascii=False, indent=2).encode('utf-8')
        st.download_button(
            label='📄 JSON Report',
            data=json_bytes,
            file_name=f'finfeex_report_{datetime.now().strftime("%Y%m%d")}.json',
            mime='application/json',
            help='Download as structured data format',
            width='stretch'
        )
        st.caption("🔧 For developers")
    
    with col_d3:
        st.download_button(
            label='📧 Email Draft',
            data=email.encode('utf-8'),
            file_name='complaint_email.txt',
            mime='text/plain',
            help='Download ready-to-send email template',
            width='stretch'
        )
        st.caption("✍️ Ready to send")
    
    # LLM Summary section (optional advanced feature)
    st.markdown("---")
    with st.expander("🤖 Want Even Deeper Insights? (AI-Powered)"):
        st.markdown("""
        <div class="info-card">
        <p>Use OpenAI's AI to get personalized recommendations and strategies to reduce your fees.</p>
        <p><strong>Note:</strong> Requires your own OpenAI API key (not stored, used only for this session).</p>
        </div>
        """, unsafe_allow_html=True)
        
        api_key = st.text_input(
            '🔑 OpenAI API Key',
            type='password',
            help="Get your API key from platform.openai.com. It's not stored anywhere.",
            placeholder="sk-..."
        )
        
        if api_key:
            if st.button('✨ Generate Personalized AI Insights', type='primary'):
                with st.spinner('🧠 AI is analyzing your fees and finding savings opportunities...'):
                    try:
                        llm_out = llm_summary(text, openai_api_key=api_key)
                        st.markdown("#### 🎯 Your Personalized Insights")
                        st.success(llm_out)
                    except Exception as e:
                        st.error(f"❌ Oops! Something went wrong: {str(e)}")
                        st.info("💡 Make sure your API key is valid and has credits available.")
    
    # Footer with helpful next steps
    st.markdown("---")
    st.markdown("""
    <div class="info-card">
    <h4>🎉 What's Next?</h4>
    <ol>
    <li><strong>Send the email</strong> to your bank (don't forget to personalize it!)</li>
    <li><strong>Track your statements</strong> over time using our Analytics page</li>
    <li><strong>Compare with other banks</strong> using our Comparison tool</li>
    <li><strong>Share FinFeeX</strong> with friends who might be overpaying too!</li>
    </ol>
    <p style="margin-top: 1rem; color: #666;"><em>Remember: Every fee you question is a step towards financial transparency. You've got this! 💪</em></p>
    </div>
    """, unsafe_allow_html=True)

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
