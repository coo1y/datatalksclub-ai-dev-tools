# Football Scoreboard — Backend

FastAPI application API that sits between the frontend and a (future) sports-data
provider, matching the `MatchDataProvider` shape the frontend already expects.

Backed by PostgreSQL (`app/db/`). The dataset is still generated deterministically —
`app/data/` is now just the seed source: on first boot the app creates the schema and,
if the `leagues` table is empty, loads the generated leagues/teams/matches into Postgres.
Routers read from the database (`app/db/repository.py`) from then on, not from Python
lists in memory.

## Run everything (Postgres + API) with Docker

```bash
docker compose up --build
```

API docs: http://localhost:8000/docs

## Run locally against a Postgres you manage yourself

```bash
uv sync
cp .env.example .env   # edit DATABASE_URL if your Postgres isn't on localhost:5432
uv run uvicorn app.main:app --reload
```

## Test

Tests don't need Postgres or Docker — they run the exact same startup/seed path against
a throwaway SQLite database instead, so the suite stays hermetic and fast:

```bash
uv run pytest
```

## Endpoints

- `GET /health`
- `GET /api/leagues`
- `GET /api/leagues/{id}`
- `GET /api/leagues/{id}/standings`
- `GET /api/teams?leagueId=&query=`
- `GET /api/teams/{id}`
- `GET /api/matches?status=&leagueId=&teamId=`
- `GET /api/matches/{id}`
- `PATCH /api/matches/{id}` — partial update of `status`, `minute`, `stoppageMinute`, `score`
- `POST /api/matches/{id}/events` — record a goal (scorer + optional assist), card, or
  substitution; a goal also bumps `score` for `teamId` automatically

All response bodies use camelCase field names to match the frontend's TypeScript types
in `frontend/src/types/`.

## Notes / next steps

- Schema is created with `SQLModel.metadata.create_all()` on startup, not migrations.
  There's no Alembic yet — once the schema needs to evolve after real data has been
  written, add Alembic rather than relying on `create_all`.
- Swapping the seed source for a real sports-data provider later means changing
  `app/db/seed.py` (or replacing it with a sync job) — `app/db/repository.py` and the
  routers don't need to change.
