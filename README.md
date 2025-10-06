# 💰 FinFeeX – Hidden-Fees X-Ray

> *“Unmasking the hidden costs behind every financial statement.”*

---

## 🧭 Overview

FinFeeX is an AI-powered tool that scans your bank or fintech statements to **detect hidden charges**, **explain them in plain language**, and **auto-draft complaint emails**. It transforms financial opacity into transparency, empowering users to know exactly where their money goes.

---

## 🎯 Problem

Financial institutions often bury small, recurring “junk” fees — like convenience fees, FX markups, or service renewals — deep within statements and T&Cs. These charges often go unnoticed but collectively cost users thousands annually.

---

## 💡 Solution

FinFeeX uses **PDF parsing + NLP + LLM summarization** to:

* Extract fee-related lines from statements
* Detect ambiguous or repeated charges
* Estimate the **true annual cost**
* Generate a **Fee Nutrition Label**
* Draft a **ready-to-send complaint/cancellation email**

---

## ⚙️ Tech Stack

| Component            | Technology                              |
| -------------------- | --------------------------------------- |
| **Frontend**         | Streamlit (for upload UI and dashboard) |
| **Backend**          | Python (Flask optional)                 |
| **Text Extraction**  | `pdfplumber` / `PyPDF2`                 |
| **NLP + Logic**      | Regex, SpaCy                            |
| **AI Summarization** | OpenAI GPT / Llama 3 / Gemma            |
| **Visualization**    | Plotly / Streamlit components           |
| **Deployment**       | Streamlit Cloud / Render / Vercel       |

---

## 🚀 Quick Start

### 1️⃣ Clone the Repo

```powershell
git clone https://github.com/<your-username>/FinFeeX.git
cd FinFeeX
```

### 2️⃣ Install Dependencies

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3️⃣ Run the App

```powershell
streamlit run app.py
```

---

## 📄 Usage

1. **Upload your statement (PDF)**
	→ FinFeeX extracts text and finds all fee-related lines.

2. **View Fee Nutrition Label**
	→ See breakdown by type: Convenience Fee, Renewal Fee, FX Markup, etc.

3. **Check True Annual Cost**
	→ Automatically calculates yearly burn from recurring or hidden charges.

4. **Copy Complaint Draft**
	→ One-click to copy a pre-drafted email for your bank/fintech provider.

---

## 🧠 Example Output

```
Hidden Charges Detected:
- Convenience Fee (Monthly): ₹49
- FX Markup: ₹300
- Renewal Fee: ₹500
Total Estimated Annual Cost: ₹1,088
Transparency Score: 68%
```

**AI Summary:**

> You’re paying ₹1,088 annually in hidden or unclear charges.
> Main culprits: renewal fees and FX markups.

**Suggested Action:**

> Consider switching to a zero-markup plan or requesting waiver.

**Auto-Drafted Email:**

> Dear Support,
> I noticed hidden charges such as FX markup and convenience fees on my account.
> Please clarify or remove them as per RBI’s disclosure norms.
> Regards,
> [User Name]

---

## 🧩 Folder Structure

```
FinFeeX/
│
├── app.py                  # Streamlit main app
├── backend/
│   ├── extract.py          # PDF → text logic
│   ├── detect.py           # Regex + fee detection logic
│   ├── summarize.py        # LLM summarizer and email generator
│
├── data/
│   ├── sample_statement.pdf
│
├── requirements.txt
└── README.md
```

---

## 🎥 Demo Flow (5 min)

1. **Intro:** Hidden fees problem (30s)
2. **Upload Statement:** Drop a PDF → instant detection (2 min)
3. **Show Fee Nutrition Label:** Visual summary of hidden costs (1 min)
4. **Copy Complaint Draft:** Email generation demo (1 min)
5. **Wrap-up:** Impact & future scope (30s)

---

## 🔮 Future Enhancements

* Compare two bank plans to find cheaper options
* Real-time email alerts when new hidden charges appear
* OpenBanking integration to fetch statements automatically
* Public “Transparency Scoreboard” for banks/fintechs

---

## 🏁 Hackathon Pitch (Short Summary)

> **FinFeeX** is your AI-powered *Hidden Fee X-Ray*.
> Upload any financial statement — it automatically extracts all fees, explains them in plain English, computes your true annual cost, and drafts a complaint email — all in seconds.
> Simple, relatable, and impactful — empowering financial transparency for everyone.

---


