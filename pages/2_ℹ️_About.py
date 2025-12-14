import streamlit as st

st.set_page_config(page_title="About FinFeeX", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About FinFeeX")

st.markdown("""
## 💰 What is FinFeeX?

**FinFeeX** is an open-source tool that helps you discover hidden fees in your financial statements. 
We believe in **financial transparency** and empowering consumers to understand where their money goes.

---

## 🎯 Our Mission

To make financial statements transparent and understandable for everyone. Hidden fees cost consumers 
thousands annually — we're here to change that.

---

## 🔍 How Does It Work?

1. **Upload**: Drop your PDF or TXT statement
2. **Analyze**: Our AI detects fee patterns and keywords
3. **Calculate**: Estimates annual impact of each fee
4. **Act**: Auto-generates complaint emails with evidence

---

## 🔒 Privacy & Security

- ✅ **No data storage**: Files are processed in-memory only
- ✅ **No tracking**: We don't collect personal information
- ✅ **Open source**: Audit our code on GitHub
- ✅ **Local-first**: Run on your own computer

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **PDF Parsing**: pdfplumber, PyPDF2
- **Data Processing**: pandas
- **Fee Detection**: Regex + NLP patterns
- **Optional AI**: OpenAI GPT (user's API key)

---

## 👥 Contributing

We welcome contributions! Check out our [GitHub repository](https://github.com/JosephJonathanFernandes/FinFeeX) 
to report issues, suggest features, or submit pull requests.

---

## 📜 License

MIT License — Free to use, modify, and distribute.

---

## 📧 Contact

Questions? Suggestions? Reach out:
- GitHub: [@JosephJonathanFernandes](https://github.com/JosephJonathanFernandes)
- Issues: [Report a bug](https://github.com/JosephJonathanFernandes/FinFeeX/issues)

---

**Made with ❤️ for financial transparency**
""")

st.balloons()
