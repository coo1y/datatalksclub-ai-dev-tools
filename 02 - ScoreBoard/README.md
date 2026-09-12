# Football Scoreboard

A football/soccer scoreboard web app: a Next.js frontend for browsing leagues, teams,
and live matches, backed by a FastAPI + PostgreSQL API that serves match data and
accepts live updates (score changes, goals, cards, substitutions).

```text
frontend (Next.js, :3000)  →  backend (FastAPI, :8000)  →  PostgreSQL
```

The dataset is generated deterministically and seeded into Postgres on first boot
(`backend/app/db/seed.py`), so the app is fully usable without a real sports-data
provider. Match IDs, team IDs, and player IDs are stable across restarts because
they're derived from the seed data, not randomly generated.

## Project layout

```text
backend/    FastAPI application + PostgreSQL models (see backend/README.md)
frontend/   Next.js application (see frontend/README.md)
api_command/  Example curl commands for driving the live-match API
_docs/specs.md  Original product spec for the frontend MVP
```

## Running the app

Start the backend first (Postgres + API in Docker):

```bash
cd backend
docker compose up --build
```

This serves the API at `http://localhost:8000` (interactive docs at
`http://localhost:8000/docs`).

Alternatively, run the API locally against a Postgres instance you manage yourself
(no Docker for the API, just for Postgres if you need one):

```bash
cd backend
uv sync
cp .env.example .env   # edit DATABASE_URL if your Postgres isn't on localhost:5432
uv run uvicorn app.main:app --reload
```

Then start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. The frontend talks to the backend at
`http://localhost:8000` by default; set `NEXT_PUBLIC_API_BASE_URL` in
`frontend/.env.local` to point elsewhere, or `NEXT_PUBLIC_USE_MOCK_API=true` to use
the frontend's in-memory mock data instead of the real backend.

## Updating a live match

Matches don't update themselves — there's no real sports-data feed wired up yet. To
simulate a live match, drive it by calling the backend API directly (with `curl`, the
Swagger UI at `/docs`, or any HTTP client). There are two things you update: **scoring
events** (who scored, or a card/substitution) and the **scoreboard state** (status,
clock, and score).

### 1. Recording a scorer (goal / card / substitution)

`POST /api/matches/{matchId}/events` appends an event to the match timeline. For a
`goal`, the backend automatically increments `score.home` or `score.away` for
`teamId` — you don't need a separate call to bump the score.

```bash
curl -X POST http://localhost:8000/api/matches/epl-r11-tottenham-liverpool/events \
  -H "Content-Type: application/json" \
  -d '{
        "minute": 61,
        "type": "goal",
        "teamId": "liverpool",
        "playerId": "liverpool-p12",
        "assistPlayerId": "liverpool-p9"
      }'
```

(See `api_command/example_update_scorer.txt` for this same example.)

Request fields (`MatchEventCreate` in `backend/app/models/match.py`):

| Field              | Required for                       | Notes                                   |
|--------------------|-------------------------------------|------------------------------------------|
| `minute`           | always                              | Match minute the event happened.         |
| `stoppageMinute`   | optional                            | e.g. `2` for `90+2'`.                    |
| `type`             | always                              | `goal`, `yellow_card`, `red_card`, or `substitution`. |
| `teamId`           | always                              | Must be the home or away team of the match. |
| `playerId`         | `goal`, `yellow_card`, `red_card`   | The scorer / carded player.              |
| `assistPlayerId`   | optional, `goal` only               | Omit if unassisted.                      |
| `playerInId` / `playerOutId` | `substitution`             | Both required for a substitution.        |

The response is the full updated `Match`, including the new event and (for goals) the
updated `score`. A `400` means a validation rule was violated (e.g. team not in this
match, or a missing required player id); a `404` means the match doesn't exist.

### 2. Updating the scoreboard (status, clock, score)

`PATCH /api/matches/{matchId}` is a partial update for the match's live state —
useful for kicking a match off, advancing the clock, moving to half-time/full-time, or
correcting the score directly instead of via an event.

```bash
curl -X PATCH http://localhost:8000/api/matches/epl-r11-tottenham-liverpool \
  -H "Content-Type: application/json" \
  -d '{
        "status": "live",
        "minute": 61
      }'
```

Request fields (`MatchUpdate`), all optional — only the fields you send are changed:

| Field             | Notes                                                                 |
|-------------------|------------------------------------------------------------------------|
| `status`          | `scheduled`, `live`, `halftime`, `finished`, `postponed`, `cancelled`. |
| `minute`          | Current match minute.                                                  |
| `stoppageMinute`  | Stoppage-time minute, if any.                                          |
| `score`           | `{ "home": <int>, "away": <int> }` — sets the score directly.          |

Prefer the `/events` endpoint over manually patching `score` when a goal happens, so
the goal also shows up in the match timeline the frontend renders.

### Finding IDs

- **Match ID**: `{leagueId}-r{round}-{homeTeamId}-{awayTeamId}`, e.g.
  `epl-r11-tottenham-liverpool`. List matches with `GET /api/matches` to browse them.
- **Team ID**: short slug, e.g. `liverpool`, `tottenham`. `GET /api/teams` lists all
  teams.
- **Player ID**: `{teamId}-p{n}`, e.g. `liverpool-p12`. Player IDs for a given match's
  squads are in that match's `lineups` (`GET /api/matches/{id}`).

Frontend changes (score, new event, status) appear on refresh/poll; the frontend does
not yet subscribe to push updates from the backend (see `backend/README.md` and
`_docs/specs.md` for the planned real-time architecture).

## Testing

```bash
cd backend
uv run pytest
```

Backend tests run against a throwaway SQLite database via the same startup/seed path
as production, so they don't need Postgres or Docker.

## Learn more

- `backend/README.md` — backend setup, endpoints, and architecture notes.
- `frontend/README.md` — frontend setup and environment variables.
- `_docs/specs.md` — original product specification for the frontend MVP.
