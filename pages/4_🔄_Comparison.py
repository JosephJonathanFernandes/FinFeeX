import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bank Comparison", page_icon="🔄", layout="wide")

st.title("🔄 Bank Comparison Tool")

st.markdown("""
Compare fees across different banks to find the best deal for your needs.
Upload statements from different banks and see side-by-side comparisons.
""")

# Check if we have history to compare
if 'fee_history' not in st.session_state or len(st.session_state.fee_history) < 2:
    st.warning("📊 You need at least 2 statements analyzed to compare. Upload statements on the main page first!")
    
    st.markdown("---")
    st.markdown("### 🎯 What You Can Compare")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 💰 Fee Totals
        - Total annual costs
        - Average fee amounts
        - Hidden charges
        """)
    
    with col2:
        st.markdown("""
        #### 📊 By Category
        - FX fees comparison
        - Transaction costs
        - Maintenance charges
        """)
    
    with col3:
        st.markdown("""
        #### 💡 Savings
        - Potential savings
        - Best value bank
        - Cost differences
        """)

else:
    # Show comparison
    statements = st.session_state.fee_history
    
    st.success(f"✅ Comparing {len(statements)} statement(s)")
    
    # Create comparison dataframe
    comparison_data = []
    for stmt in statements:
        fees_df = pd.DataFrame(stmt['fees'])
        total = fees_df['annual_cost_estimate'].sum() if 'annual_cost_estimate' in fees_df.columns else 0
        avg = fees_df['annual_cost_estimate'].mean() if 'annual_cost_estimate' in fees_df.columns else 0
        count = len(fees_df)
        
        # Category breakdown
        if 'category' in fees_df.columns:
            cat_totals = fees_df.groupby('category')['annual_cost_estimate'].sum().to_dict()
        else:
            cat_totals = {}
        
        comparison_data.append({
            'Statement': stmt['name'],
            'Date': stmt['date'],
            'Total Annual Cost': total,
            'Average Fee': avg,
            'Fee Count': count,
            'Categories': cat_totals
        })
    
    comp_df = pd.DataFrame(comparison_data)
    
    # Overall comparison metrics
    st.markdown("### 📊 Overall Comparison")
    
    cols = st.columns(len(statements))
    for idx, (col, row) in enumerate(zip(cols, comparison_data)):
        with col:
            is_best = row['Total Annual Cost'] == comp_df['Total Annual Cost'].min()
            color = "green" if is_best else "blue"
            st.markdown(f"**{row['Statement']}**")
            st.metric("Total Annual", f"₹{int(row['Total Annual Cost']):,}", 
                     delta="Best Deal!" if is_best else None,
                     delta_color="normal" if is_best else "off")
            st.metric("Avg Fee", f"₹{int(row['Average Fee']):,}")
            st.metric("Fee Count", row['Fee Count'])
    
    # Savings calculation
    st.markdown("---")
    st.markdown("### 💰 Potential Savings")
    
    min_cost = comp_df['Total Annual Cost'].min()
    max_cost = comp_df['Total Annual Cost'].max()
    savings = max_cost - min_cost
    
    if savings > 0:
        best_bank = comp_df.loc[comp_df['Total Annual Cost'].idxmin(), 'Statement']
        worst_bank = comp_df.loc[comp_df['Total Annual Cost'].idxmax(), 'Statement']
        
        st.success(f"""
        💡 **Insight**: Switching from **{worst_bank}** to **{best_bank}** could save you 
        **₹{int(savings):,}** per year!
        """)
    
    # Visual comparison
    st.markdown("---")
    st.markdown("### 📊 Visual Comparison")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### Total Costs Comparison")
        fig = px.bar(comp_df, x='Statement', y='Total Annual Cost',
                    color='Total Annual Cost',
                    color_continuous_scale='Purples')
        fig.update_layout(showlegend=False, yaxis_title="Annual Cost (₹)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_b:
        st.markdown("#### Fee Count Comparison")
        fig = px.bar(comp_df, x='Statement', y='Fee Count',
                    color='Fee Count',
                    color_continuous_scale='Teal')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Category breakdown
    st.markdown("---")
    st.markdown("### 📋 Category Breakdown")
    
    # Prepare category comparison data
    all_categories = set()
    for row in comparison_data:
        all_categories.update(row['Categories'].keys())
    
    cat_comparison = []
    for cat in all_categories:
        row_data = {'Category': cat}
        for stmt in comparison_data:
            row_data[stmt['Statement']] = stmt['Categories'].get(cat, 0)
        cat_comparison.append(row_data)
    
    cat_df = pd.DataFrame(cat_comparison)
    
    if not cat_df.empty:
        fig = px.bar(cat_df, x='Category', y=[col for col in cat_df.columns if col != 'Category'],
                    barmode='group', color_discrete_sequence=px.colors.sequential.Purples)
        fig.update_layout(yaxis_title="Annual Cost (₹)", xaxis_title="Fee Category")
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.markdown("---")
    st.markdown("### 📄 Detailed Comparison Table")
    st.dataframe(comp_df[['Statement', 'Date', 'Total Annual Cost', 'Average Fee', 'Fee Count']], 
                width='stretch', hide_index=True)
