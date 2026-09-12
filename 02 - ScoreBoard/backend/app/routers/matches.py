from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.db import get_session
from app.db import repository
from app.models import Match, MatchEventCreate, MatchStatus, MatchUpdate

router = APIRouter(prefix="/api/matches", tags=["matches"])


@router.get("", response_model=List[Match])
def list_matches(
    status: Optional[List[MatchStatus]] = Query(None),
    league_id: Optional[str] = Query(None, alias="leagueId"),
    team_id: Optional[str] = Query(None, alias="teamId"),
    session: Session = Depends(get_session),
) -> List[Match]:
    return repository.list_matches(session, statuses=status, league_id=league_id, team_id=team_id)


@router.get("/{match_id}", response_model=Match)
def get_match(match_id: str, session: Session = Depends(get_session)) -> Match:
    match = repository.get_match(session, match_id)
    if match is None:
        raise HTTPException(status_code=404, detail=f"Match not found: {match_id}")
    return match


@router.patch("/{match_id}", response_model=Match)
def update_match(match_id: str, update: MatchUpdate, session: Session = Depends(get_session)) -> Match:
    match = repository.update_match(session, match_id, update)
    if match is None:
        raise HTTPException(status_code=404, detail=f"Match not found: {match_id}")
    return match


@router.post("/{match_id}/events", response_model=Match, status_code=201)
def add_match_event(match_id: str, event: MatchEventCreate, session: Session = Depends(get_session)) -> Match:
    try:
        match = repository.add_match_event(session, match_id, event)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if match is None:
        raise HTTPException(status_code=404, detail=f"Match not found: {match_id}")
    return match
