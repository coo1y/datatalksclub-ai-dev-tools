from typing import List, Optional

from app.models import League

CURRENT_SEASON = "2026/27"

LEAGUES: List[League] = [
    League(id="epl", name="Premier League", short_name="EPL", country="England",
           logo_url=None, scope="domestic", is_supported=True, season=CURRENT_SEASON),
    League(id="laliga", name="La Liga", short_name="La Liga", country="Spain",
           logo_url=None, scope="domestic", is_supported=True, season=CURRENT_SEASON),
    League(id="ucl", name="UEFA Champions League", short_name="UCL", country="Europe",
           logo_url=None, scope="european", is_supported=True, season=CURRENT_SEASON),
    League(id="seriea", name="Serie A", short_name="Serie A", country="Italy",
           logo_url=None, scope="domestic", is_supported=True, season=CURRENT_SEASON),
    League(id="bundesliga", name="Bundesliga", short_name="Bundesliga", country="Germany",
           logo_url=None, scope="domestic", is_supported=True, season=CURRENT_SEASON),
    League(id="ligue1", name="Ligue 1", short_name="Ligue 1", country="France",
           logo_url=None, scope="domestic", is_supported=True, season=CURRENT_SEASON),
    League(id="intl-friendlies", name="International Friendlies", short_name="Int'l Friendlies",
           country="World", logo_url=None, scope="international", is_supported=True, season=CURRENT_SEASON),
    # Not yet backed by real data -- shown as "Coming soon" and non-interactive on the frontend.
    League(id="mls", name="Major League Soccer", short_name="MLS", country="USA",
           logo_url=None, scope="domestic", is_supported=False, season=CURRENT_SEASON),
    League(id="eredivisie", name="Eredivisie", short_name="Eredivisie", country="Netherlands",
           logo_url=None, scope="domestic", is_supported=False, season=CURRENT_SEASON),
    League(id="primeira-liga", name="Primeira Liga", short_name="Primeira Liga", country="Portugal",
           logo_url=None, scope="domestic", is_supported=False, season=CURRENT_SEASON),
    League(id="championship", name="EFL Championship", short_name="Championship", country="England",
           logo_url=None, scope="domestic", is_supported=False, season=CURRENT_SEASON),
    League(id="brasileirao", name="Brasileirão", short_name="Brasileirão", country="Brazil",
           logo_url=None, scope="domestic", is_supported=False, season=CURRENT_SEASON),
]

_LEAGUES_BY_ID = {league.id: league for league in LEAGUES}


def get_league_by_id(league_id: str) -> Optional[League]:
    return _LEAGUES_BY_ID.get(league_id)
