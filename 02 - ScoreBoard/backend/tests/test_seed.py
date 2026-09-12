from sqlmodel import Session, select

from app.data import LEAGUES, MATCHES, TEAMS
from app.db.session import engine
from app.db.tables import LeagueRow, MatchRow, TeamRow


def test_seed_persists_every_league_team_and_match(client):
    """`client` triggers the app's lifespan (create tables + seed) before this runs."""
    with Session(engine) as session:
        assert len(session.exec(select(LeagueRow)).all()) == len(LEAGUES)
        assert len(session.exec(select(TeamRow)).all()) == len(TEAMS)
        assert len(session.exec(select(MatchRow)).all()) == len(MATCHES)


def test_seed_is_idempotent(client):
    from app.db.seed import seed_if_empty

    with Session(engine) as session:
        seed_if_empty(session)
        seed_if_empty(session)
        assert len(session.exec(select(LeagueRow)).all()) == len(LEAGUES)
