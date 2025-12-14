import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Fee Analytics", page_icon="📊", layout="wide")

st.title("📊 Fee Analytics Dashboard")

# Initialize session state for historical tracking
if 'fee_history' not in st.session_state:
    st.session_state.fee_history = []

# Check if we have any data
if not st.session_state.fee_history:
    st.info("💡 **Tip**: Analyze statements on the main page first. Your fee history will appear here for comparison and trend analysis.")
    
    # Show sample analytics preview
    st.markdown("### 🎯 What You'll See Here")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📈 Historical Tracking
        - Track fees across multiple statements
        - See how charges change over time
        - Identify trends and patterns
        
        #### 💰 Cost Breakdown
        - Fees by category
        - Monthly vs annual comparisons
        - Highest cost offenders
        """)
    
    with col2:
        st.markdown("""
        #### 🔄 Bank Comparison
        - Compare fees between institutions
        - Find the best deals
        - Calculate potential savings
        
        #### 📊 Visual Insights
        - Interactive charts
        - Trend analysis
        - Predictive estimates
        """)
    
    # Sample visualization
    st.markdown("---")
    st.markdown("### 📊 Sample Visualization")
    
    sample_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Total Fees': [580, 620, 550, 590, 610, 580],
        'Transaction Fees': [200, 220, 190, 210, 220, 200],
        'FX Markup': [180, 200, 160, 180, 190, 180],
        'Annual Fees': [200, 200, 200, 200, 200, 200]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sample_data['Month'], y=sample_data['Total Fees'], 
                             mode='lines+markers', name='Total Fees',
                             line=dict(color='#667eea', width=3)))
    fig.update_layout(title='Sample: Fee Trends Over Time', 
                     xaxis_title='Month', yaxis_title='Fees (₹)',
                     height=400)
    st.plotly_chart(fig, use_container_width=True)
    
else:
    # Show actual analytics from session state
    st.success(f"✅ Tracking {len(st.session_state.fee_history)} statement(s)")
    
    # Aggregate all fees
    all_fees = []
    for entry in st.session_state.fee_history:
        for fee in entry['fees']:
            fee_copy = fee.copy()
            fee_copy['date'] = entry['date']
            fee_copy['statement'] = entry['name']
            all_fees.append(fee_copy)
    
    df = pd.DataFrame(all_fees)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = df['annual_cost_estimate'].sum() if 'annual_cost_estimate' in df.columns else 0
        st.metric("Total Annual Fees", f"₹{int(total):,}")
    
    with col2:
        avg = df['annual_cost_estimate'].mean() if 'annual_cost_estimate' in df.columns else 0
        st.metric("Average Fee", f"₹{int(avg):,}")
    
    with col3:
        st.metric("Unique Fees", len(df))
    
    with col4:
        categories = df['category'].nunique() if 'category' in df.columns else 0
        st.metric("Categories", categories)
    
    st.markdown("---")
    
    # Visualizations
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### 📊 Fees by Category")
        if 'category' in df.columns and 'annual_cost_estimate' in df.columns:
            cat_data = df.groupby('category')['annual_cost_estimate'].sum().sort_values(ascending=False)
            fig = px.pie(values=cat_data.values, names=cat_data.index, 
                        color_discrete_sequence=px.colors.sequential.Purples_r)
            st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        st.markdown("#### 📈 Trend Analysis")
        if len(st.session_state.fee_history) > 1:
            trend_data = pd.DataFrame([
                {'Date': entry['date'], 'Total': sum(f.get('annual_cost_estimate', 0) for f in entry['fees'])}
                for entry in st.session_state.fee_history
            ])
            fig = px.line(trend_data, x='Date', y='Total', markers=True,
                         line_shape='spline', color_discrete_sequence=['#667eea'])
            fig.update_layout(yaxis_title='Annual Cost (₹)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Upload more statements to see trends")
    
    # Detailed table
    st.markdown("---")
    st.markdown("#### 📋 All Detected Fees")
    if 'category' in df.columns:
        display_cols = ['statement', 'category', 'line', 'type', 'value', 'annual_cost_estimate']
        display_df = df[[c for c in display_cols if c in df.columns]]
        st.dataframe(display_df, width='stretch', hide_index=True)
    
    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state.fee_history = []
        st.rerun()
