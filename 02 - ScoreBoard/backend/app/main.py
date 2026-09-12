from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from app.db import create_db_and_tables, engine
from app.db.seed import seed_if_empty
from app.routers import leagues, matches, teams


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        seed_if_empty(session)
    yield


app = FastAPI(title="Football Scoreboard API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(leagues.router)
app.include_router(teams.router)
app.include_router(matches.router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
