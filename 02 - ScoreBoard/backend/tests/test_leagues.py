def test_list_leagues_returns_all_leagues(client):
    response = client.get("/api/leagues")

    assert response.status_code == 200
    body = response.json()
    ids = [league["id"] for league in body]
    assert "epl" in ids
    assert "mls" in ids
    assert len(body) >= 7


def test_list_leagues_includes_unsupported_flag(client):
    response = client.get("/api/leagues")

    body = response.json()
    epl = next(league for league in body if league["id"] == "epl")
    mls = next(league for league in body if league["id"] == "mls")

    assert epl["isSupported"] is True
    assert mls["isSupported"] is False


def test_list_leagues_uses_camel_case_fields(client):
    response = client.get("/api/leagues")

    epl = next(league for league in response.json() if league["id"] == "epl")
    assert set(["id", "name", "shortName", "country", "logoUrl", "scope", "isSupported", "season"]).issubset(
        epl.keys()
    )


def test_get_league_by_id_returns_league(client):
    response = client.get("/api/leagues/epl")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "epl"
    assert body["name"] == "Premier League"


def test_get_league_by_id_not_found(client):
    response = client.get("/api/leagues/does-not-exist")

    assert response.status_code == 404
    assert "does-not-exist" in response.json()["detail"]


def test_get_standings_returns_ranked_table(client):
    response = client.get("/api/leagues/epl/standings")

    assert response.status_code == 200
    body = response.json()
    assert len(body) > 0

    positions = [row["position"] for row in body]
    assert positions == sorted(positions)
    assert positions[0] == 1

    for row in body:
        assert row["leagueId"] == "epl"
        assert row["played"] == row["won"] + row["drawn"] + row["lost"]
        assert row["goalDifference"] == row["goalsFor"] - row["goalsAgainst"]
        assert row["points"] == row["won"] * 3 + row["drawn"]

    points = [row["points"] for row in body]
    assert points == sorted(points, reverse=True)


def test_get_standings_for_unknown_league_returns_empty_list(client):
    response = client.get("/api/leagues/does-not-exist/standings")

    assert response.status_code == 200
    assert response.json() == []
