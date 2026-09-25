install:
	python -m pip install -r requirements.txt

run:
	python slavic_cognitive_agent.py

interactive:
	python slavic_cognitive_agent.py --interactive

api:
	uvicorn app.main:app --reload

test:
	pytest -q

docker-up:
	docker compose up --build
