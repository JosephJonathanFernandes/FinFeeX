import streamlit as st

st.set_page_config(page_title="FAQ", page_icon="❓", layout="wide")

st.title("❓ Frequently Asked Questions")

with st.expander("🔍 What types of fees does FinFeeX detect?"):
    st.markdown("""
    FinFeeX can detect various hidden fees including:
    - Convenience fees
    - Processing charges
    - Foreign exchange markups
    - Annual/renewal fees
    - Service charges
    - Late payment penalties
    - Minimum balance charges
    - And more...
    """)

with st.expander("🔒 Is my financial data safe?"):
    st.markdown("""
    **Absolutely!** Your data privacy is our priority:
    - Files are processed locally in your browser/server
    - No data is stored or transmitted to external servers
    - We don't collect any personal information
    - The app is open source — you can verify the code yourself
    """)

with st.expander("📄 What file formats are supported?"):
    st.markdown("""
    Currently supported formats:
    - **PDF**: Most common bank statement format
    - **TXT**: Plain text exports from online banking
    
    Coming soon: CSV, Excel, and direct bank API integration!
    """)

with st.expander("💰 How accurate are the fee calculations?"):
    st.markdown("""
    Our detection is highly accurate for clearly stated fees. However:
    - Percentage fees require you to estimate transaction volume
    - Some fees may be missed if using non-standard terminology
    - Always verify results against your actual statement
    
    We're continuously improving our detection algorithms!
    """)

with st.expander("📧 Can I customize the complaint email?"):
    st.markdown("""
    Yes! The email is just a template:
    - Copy the text and edit as needed
    - Add your personal details (name, account number)
    - Adjust the tone to match your preference
    - Include specific dates and amounts
    """)

with st.expander("🌍 Does it work with international statements?"):
    st.markdown("""
    Currently optimized for Indian Rupees (₹), but:
    - Detection works with most currencies
    - Supports multiple currency symbols
    - Keywords work for English statements
    
    Multilingual support coming soon!
    """)

with st.expander("🤖 What is the AI Summary feature?"):
    st.markdown("""
    The optional AI Summary uses OpenAI's GPT to:
    - Provide natural language insights
    - Suggest money-saving actions
    - Explain complex fee structures
    
    **Note**: Requires your own OpenAI API key (not included)
    """)

with st.expander("💡 How can I get better results?"):
    st.markdown("""
    Tips for best results:
    - Upload clear, complete statements
    - Adjust the annual transaction estimate for % fees
    - Review the Fee Nutrition Label for accuracy
    - Compare multiple statements to track trends
    """)

with st.expander("🐛 I found a bug or have a suggestion"):
    st.markdown("""
    We'd love to hear from you!
    - Report bugs on [GitHub Issues](https://github.com/JosephJonathanFernandes/FinFeeX/issues)
    - Suggest features via pull requests
    - Star the repo if you find it useful ⭐
    """)

with st.expander("📜 Is this really free?"):
    st.markdown("""
    **100% Free and Open Source!**
    - No hidden costs
    - No premium tiers
    - No subscription required
    - MIT License — use freely
    
    If you find it valuable, consider:
    - ⭐ Starring the GitHub repo
    - 🔄 Sharing with friends
    - 🤝 Contributing code improvements
    """)

st.markdown("---")
st.success("💬 Still have questions? Open an issue on our [GitHub repository](https://github.com/JosephJonathanFernandes/FinFeeX)!")
