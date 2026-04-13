FROM python:3.11-slim-buster AS builder

WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim-buster
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /app/src/

ENV PYTHONPATH=/app/src
CMD ["uvicorn", "nexustask.interfaces.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
