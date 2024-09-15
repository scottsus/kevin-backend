# 🚀 Blazingly fast Python server template

Lightweight, only with FastAPI + SQLModel + Alembic + Postgres - and blazingly fast.

## Quick Start

Start the Docker containers and visit `http://localhost:8004` for a quick health check.

```
docker-compose up -d --build
docker-compose exec web alembic upgrade head

# Destroy the container
docker-compose down -v
```

This spins up a `web` FastAPI + SQLModel + Alembic container, and a `db` Postgres container out of the box.

## Scripts

1. Generate a migration

   ```
   docker-compose exec web alembic revision --autogenerate "{MIGRATION_NAME}"
   ```

2. Apply migration

   ```
   docker-compose exec web alembic upgrade head
   ```

3. Undo migration

   ```
   docker-compose exec web alembic downgrade -1
   ```

4. Inspect Postgres container

   ```
   docker-compose exec db psql -U postgres
   \c foo
   \dt
   ```

5. Get streaming logs from web container
   ```
   docker-compose logs -f web
   ```

## Includes

### Core

1. Async FastAPI
2. SQLModel & SQLAlchemy
3. Alembic
4. Postgres
5. Docker & Docker Compose

## Pay attention to...

1. `env.py:12-13`: you need to import all models here for `--autogenerate` to function.
2. `PostgresBase`: provides a `uuid id, created_at, updated_at` for every model that inherits it.
