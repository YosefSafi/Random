.PHONY: setup test lint run build docker-build helm-deploy migrate

setup:
	poetry install
	pre-commit install

test:
	poetry run pytest tests/ -n auto --cov=src

lint:
	poetry run black src tests
	poetry run isort src tests
	poetry run mypy src
	poetry run flake8 src

run-api:
	poetry run uvicorn nexustask.interfaces.api.main:app --reload

run-worker:
	poetry run celery -A nexustask.infrastructure.worker.celery_app worker -l info

migrate:
	poetry run alembic upgrade head

docker-build:
	docker build -t nexustask/core:latest -f deployments/docker/Dockerfile .

helm-deploy:
	helm upgrade --install nexustask ./deployments/kubernetes/helm/nexustask
