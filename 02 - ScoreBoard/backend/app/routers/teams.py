from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.db import get_session
from app.db import repository
from app.models import Team

router = APIRouter(prefix="/api/teams", tags=["teams"])


@router.get("", response_model=List[Team])
def list_teams(
    league_id: Optional[str] = Query(None, alias="leagueId"),
    query: Optional[str] = Query(None),
    session: Session = Depends(get_session),
) -> List[Team]:
    return repository.list_teams(session, league_id=league_id, query=query)


@router.get("/{team_id}", response_model=Team)
def get_team(team_id: str, session: Session = Depends(get_session)) -> Team:
    team = repository.get_team(session, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail=f"Team not found: {team_id}")
    return team
