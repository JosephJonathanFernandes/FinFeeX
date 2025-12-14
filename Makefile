.PHONY: venv install test run clean docker-build docker-run

venv:
	python -m venv .venv

install: venv
	.\.venv\Scripts\Activate.ps1; pip install --upgrade pip; pip install -r requirements.txt

test:
	.\.venv\Scripts\Activate.ps1; pytest -q

run:
	.\.venv\Scripts\Activate.ps1; streamlit run app.py

clean:
	Remove-Item -Recurse -Force .venv, __pycache__, .pytest_cache, src/__pycache__, tests/__pycache__ -ErrorAction SilentlyContinue

docker-build:
	docker build -t finfeex:latest .

docker-run:
	docker run -p 8501:8501 finfeex:latest
