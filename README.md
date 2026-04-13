# NexusTask Enterprise Edition

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Version](https://img.shields.io/badge/version-10.4.2-blue)

NexusTask is an enterprise-grade, highly scalable, distributed task and project management system. Born in 2016, it has evolved from a simple CLI into a globally distributed ecosystem powering fortune 500 companies.

## Architecture
NexusTask utilizes a modern **Domain-Driven Design (DDD)** approach coupled with **CQRS** (Command Query Responsibility Segregation) and **Event Sourcing**.

- **Core Domain**: Pure Python, zero dependencies.
- **Infrastructure**: Async SQLAlchemy (PostgreSQL), Redis (Caching & Rate Limiting), Kafka (Event Bus), Elasticsearch (Advanced Search).
- **Interfaces**: REST API (FastAPI), GraphQL (Strawberry), gRPC, and a rich CLI (Click + Rich).

## Documentation
Read the full documentation at [docs.nexustask.io](https://docs.nexustask.io).
See the `docs/adrs/` folder for the last 10 years of Architectural Decision Records.

## Quickstart (Development)
```bash
make setup
docker-compose up -d  # Starts Postgres, Redis, Kafka, ElasticSearch
make migrate
make run-api
```

## Copyright
Copyright (c) 2016-2026 NexusTask Foundation.
