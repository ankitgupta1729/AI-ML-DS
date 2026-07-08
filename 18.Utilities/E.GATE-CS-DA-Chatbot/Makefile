.PHONY: help install dev ingest reset stats fetch api web-install web web-build test docker

help:
	@echo "Targets:"
	@echo "  install      Create .venv and install Python dependencies"
	@echo "  dev          Run BOTH backend (:8000) and frontend (:5173) together"
	@echo "  ingest       Build/refresh the vector index from data/ (incremental)"
	@echo "  reset        Wipe and rebuild the vector index"
	@echo "  stats        Show number of indexed chunks"
	@echo "  fetch        List free/open study resources (add --download to fetch)"
	@echo "  api          Run only the FastAPI backend (http://localhost:8000)"
	@echo "  web-install  Install the React frontend dependencies"
	@echo "  web          Run only the React dev server (http://localhost:5173)"
	@echo "  web-build    Build the production frontend bundle (frontend/dist)"
	@echo "  test         Run the Python test suite"
	@echo "  docker       Build and start frontend + API via docker compose"

dev:
	bash scripts/dev.sh

install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

ingest:
	python scripts/ingest.py

reset:
	python scripts/ingest.py --reset

stats:
	python scripts/ingest.py --stats

fetch:
	python scripts/fetch_open_resources.py

api:
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

web-install:
	cd frontend && npm install

web:
	cd frontend && npm run dev

web-build:
	cd frontend && npm run build

test:
	pytest -q

docker:
	docker compose up --build
