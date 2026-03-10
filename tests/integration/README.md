# Integration Tests

Integration tests require a live PostgreSQL database and real network access to the NHL API.

## Setup

1. Create a test database:
   ```sql
   CREATE DATABASE nhl_test;
   ```

2. Set the `DATABASE_URL` environment variable:
   ```bash
   export DATABASE_URL=postgresql+asyncpg://localhost/nhl_test
   ```

3. Run migrations:
   ```bash
   alembic upgrade head
   ```

4. Run integration tests:
   ```bash
   pytest tests/integration/ -v
   ```

Integration tests are excluded from the default test run to avoid requiring external services in CI.
