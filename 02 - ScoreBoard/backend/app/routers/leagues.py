from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db import get_session
from app.db import repository
from app.models import League, Standing

router = APIRouter(prefix="/api/leagues", tags=["leagues"])


@router.get("", response_model=List[League])
def list_leagues(session: Session = Depends(get_session)) -> List[League]:
    return repository.list_leagues(session)


@router.get("/{league_id}", response_model=League)
def get_league(league_id: str, session: Session = Depends(get_session)) -> League:
    league = repository.get_league(session, league_id)
    if league is None:
        raise HTTPException(status_code=404, detail=f"League not found: {league_id}")
    return league


@router.get("/{league_id}/standings", response_model=List[Standing])
def get_standings(league_id: str, session: Session = Depends(get_session)) -> List[Standing]:
    return repository.get_standings(session, league_id)
