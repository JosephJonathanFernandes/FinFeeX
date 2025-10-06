Thanks for wanting to contribute to FinFeeX! We appreciate small, focused PRs.

Guidelines:
- Open an issue first for non-trivial changes.
- Make small atomic PRs with tests.
- Follow the code style used in the project.
- Do not commit API keys or secrets.

Local dev:
```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
streamlit run app.py
```
