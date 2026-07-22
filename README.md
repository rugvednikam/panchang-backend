# Hindu Astrology REST API

A production-ready, commercial-grade Astrology Backend built with Python, FastAPI, PostgreSQL, Redis, and Swiss Ephemeris (`pyswisseph`).

## Features
- **Accurate Astronomical Engine**: Built on Swiss Ephemeris.
- **Panchang**: Tithi, Nakshatra, Yoga, Karana, Vara, Kaals.
- **Kundli**: Planetary Positions, Ascendant, Houses (D1, D9).
- **Dasha**: Vimshottari Dasha calculations.
- **Auth**: JWT Authentication and API Key Rate Limiting via Redis.
- **Async Database**: PostgreSQL via asyncpg & SQLAlchemy 2.0.

## Tech Stack
- Python 3.12+
- FastAPI & Uvicorn
- PostgreSQL & Alembic
- Redis (fastapi-limiter)
- PySwissEph (Astrology Engine)

## Getting Started (Docker)

1. Rename `.env.example` to `.env` and configure your credentials.
2. Build and start the services:
   ```bash
   docker-compose up --build -d
   ```
3. Access the OpenAPI Swagger Documentation at:
   [http://localhost:8000/docs](http://localhost:8000/docs)
4. Use the provided `postman_collection.json` to import endpoints into Postman.

## Running Migrations
To run database migrations after starting the docker containers:
```bash
docker exec -it astrology_api alembic upgrade head
```

## Running Tests
To execute the pytest suite for calculation accuracy:
```bash
docker exec -it astrology_api pytest
```
