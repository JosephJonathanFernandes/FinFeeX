venv:
	python -m venv .venv

install: venv
	. .venv/Scripts/activate && pip install -r requirements.txt

run:
	python -m streamlit run app.py

test:
	pytest -q

docker-build:
	docker build -t finfeex:latest .

docker-run:
	docker run -p 8501:8501 finfeex:latest
