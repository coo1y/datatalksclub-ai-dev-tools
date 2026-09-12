def test_list_teams_returns_all_teams(client):
    response = client.get("/api/teams")

    assert response.status_code == 200
    body = response.json()
    ids = [team["id"] for team in body]
    assert "arsenal" in ids
    assert len(body) > 20


def test_list_teams_uses_camel_case_fields(client):
    response = client.get("/api/teams")

    arsenal = next(team for team in response.json() if team["id"] == "arsenal")
    assert set(["id", "name", "shortName", "crestUrl", "country", "competitions"]).issubset(arsenal.keys())
    assert arsenal["competitions"][0].keys() == {"leagueId", "scope"}


def test_list_teams_filter_by_league(client):
    response = client.get("/api/teams", params={"leagueId": "epl"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) > 0
    for team in body:
        league_ids = [c["leagueId"] for c in team["competitions"]]
        assert "epl" in league_ids


def test_list_teams_filter_by_query_matches_name_case_insensitive(client):
    response = client.get("/api/teams", params={"query": "arse"})

    body = response.json()
    ids = [team["id"] for team in body]
    assert "arsenal" in ids
    assert all("arse" in team["name"].lower() or "arse" in team["shortName"].lower() for team in body)


def test_list_teams_filter_by_query_matches_short_name(client):
    response = client.get("/api/teams", params={"query": "ars"})

    ids = [team["id"] for team in response.json()]
    assert "arsenal" in ids


def test_get_team_by_id_returns_team(client):
    response = client.get("/api/teams/arsenal")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "arsenal"
    assert body["name"] == "Arsenal"


def test_get_team_by_id_not_found(client):
    response = client.get("/api/teams/does-not-exist")

    assert response.status_code == 404
    assert "does-not-exist" in response.json()["detail"]


def test_team_participating_in_champions_league_has_extra_competition(client):
    response = client.get("/api/teams/arsenal")

    league_ids = [c["leagueId"] for c in response.json()["competitions"]]
    assert "epl" in league_ids
    assert "ucl" in league_ids
