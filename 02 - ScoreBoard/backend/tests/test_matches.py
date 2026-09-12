VALID_STATUSES = {"scheduled", "live", "halftime", "finished", "postponed", "cancelled"}


def test_list_matches_returns_all_matches(client):
    response = client.get("/api/matches")

    assert response.status_code == 200
    body = response.json()
    assert len(body) > 0
    for match in body:
        assert match["status"] in VALID_STATUSES


def test_list_matches_uses_camel_case_fields(client):
    response = client.get("/api/matches")

    match = response.json()[0]
    assert set(["id", "league", "season", "kickoff", "status", "homeTeam", "awayTeam", "score"]).issubset(
        match.keys()
    )
    assert set(match["homeTeam"].keys()) == {"id", "name", "shortName", "crestUrl"}


def test_list_matches_filter_by_single_status(client):
    response = client.get("/api/matches", params={"status": "live"})

    body = response.json()
    assert len(body) > 0
    assert all(match["status"] == "live" for match in body)


def test_list_matches_filter_by_multiple_statuses(client):
    response = client.get("/api/matches", params=[("status", "live"), ("status", "finished")])

    body = response.json()
    assert len(body) > 0
    assert all(match["status"] in {"live", "finished"} for match in body)


def test_list_matches_filter_by_league(client):
    response = client.get("/api/matches", params={"leagueId": "epl"})

    body = response.json()
    assert len(body) > 0
    assert all(match["league"]["id"] == "epl" for match in body)


def test_list_matches_filter_by_team(client):
    all_matches = client.get("/api/matches").json()
    team_id = all_matches[0]["homeTeam"]["id"]

    response = client.get("/api/matches", params={"teamId": team_id})

    body = response.json()
    assert len(body) > 0
    assert all(match["homeTeam"]["id"] == team_id or match["awayTeam"]["id"] == team_id for match in body)


def test_scheduled_match_has_no_score_yet(client):
    response = client.get("/api/matches", params={"status": "scheduled"})

    body = response.json()
    assert len(body) > 0
    for match in body:
        assert match["score"]["home"] is None
        assert match["score"]["away"] is None


def test_finished_match_has_final_score(client):
    response = client.get("/api/matches", params={"status": "finished"})

    body = response.json()
    assert len(body) > 0
    for match in body:
        assert isinstance(match["score"]["home"], int)
        assert isinstance(match["score"]["away"], int)


def test_live_match_includes_events_lineups_and_statistics(client):
    live_matches = client.get("/api/matches", params={"status": "live"}).json()
    match_id = live_matches[0]["id"]

    response = client.get(f"/api/matches/{match_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == match_id
    assert body["minute"] is not None
    assert body["events"]
    assert body["lineups"]["home"]["startingXI"]
    assert len(body["lineups"]["home"]["startingXI"]) == 11
    assert body["statistics"]["home"]["possession"] + body["statistics"]["away"]["possession"] == 100


def test_get_match_by_id_not_found(client):
    response = client.get("/api/matches/does-not-exist")

    assert response.status_code == 404
    assert "does-not-exist" in response.json()["detail"]


def test_update_match_score(client):
    live_matches = client.get("/api/matches", params={"status": "live"}).json()
    match_id = live_matches[0]["id"]

    response = client.patch(f"/api/matches/{match_id}", json={"score": {"home": 3, "away": 1}})

    assert response.status_code == 200
    body = response.json()
    assert body["score"] == {"home": 3, "away": 1}

    refetched = client.get(f"/api/matches/{match_id}").json()
    assert refetched["score"] == {"home": 3, "away": 1}


def test_update_match_status_and_minute_leaves_score_unchanged(client):
    live_matches = client.get("/api/matches", params={"status": "live"}).json()
    match_id = live_matches[0]["id"]
    original_score = live_matches[0]["score"]

    response = client.patch(f"/api/matches/{match_id}", json={"status": "halftime", "minute": 45})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "halftime"
    assert body["minute"] == 45
    assert body["score"] == original_score


def test_update_match_not_found(client):
    response = client.patch("/api/matches/does-not-exist", json={"score": {"home": 1, "away": 0}})

    assert response.status_code == 404
    assert "does-not-exist" in response.json()["detail"]


def test_add_goal_event_records_scorer_and_bumps_score(client):
    live_matches = client.get("/api/matches", params={"status": "live"}).json()
    match_id = live_matches[0]["id"]
    match_detail = client.get(f"/api/matches/{match_id}").json()
    home_team_id = match_detail["homeTeam"]["id"]
    scorer_id = match_detail["lineups"]["home"]["startingXI"][0]["id"]
    assist_id = match_detail["lineups"]["home"]["startingXI"][1]["id"]
    original_home_score = match_detail["score"]["home"]

    response = client.post(
        f"/api/matches/{match_id}/events",
        json={
            "minute": 55,
            "type": "goal",
            "teamId": home_team_id,
            "playerId": scorer_id,
            "assistPlayerId": assist_id,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["score"]["home"] == original_home_score + 1

    new_event = next(e for e in body["events"] if e["minute"] == 55)
    assert new_event["type"] == "goal"
    assert new_event["player"]["id"] == scorer_id
    assert new_event["assistPlayer"]["id"] == assist_id


def test_add_substitution_event_does_not_change_score(client):
    live_matches = client.get("/api/matches", params={"status": "live"}).json()
    match_id = live_matches[0]["id"]
    match_detail = client.get(f"/api/matches/{match_id}").json()
    home_team_id = match_detail["homeTeam"]["id"]
    player_out = match_detail["lineups"]["home"]["startingXI"][2]["id"]
    player_in = match_detail["lineups"]["home"]["substitutes"][0]["id"]
    original_score = match_detail["score"]

    response = client.post(
        f"/api/matches/{match_id}/events",
        json={
            "minute": 70,
            "type": "substitution",
            "teamId": home_team_id,
            "playerInId": player_in,
            "playerOutId": player_out,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["score"] == original_score
    new_event = next(e for e in body["events"] if e["minute"] == 70)
    assert new_event["playerIn"]["id"] == player_in
    assert new_event["playerOut"]["id"] == player_out


def test_add_event_rejects_team_not_in_match(client):
    live_matches = client.get("/api/matches", params={"status": "live"}).json()
    match_id = live_matches[0]["id"]

    response = client.post(
        f"/api/matches/{match_id}/events",
        json={"minute": 10, "type": "goal", "teamId": "not-a-real-team", "playerId": "some-player"},
    )

    assert response.status_code == 400


def test_add_event_to_missing_match_returns_404(client):
    response = client.post(
        "/api/matches/does-not-exist/events",
        json={"minute": 10, "type": "goal", "teamId": "team", "playerId": "player"},
    )

    assert response.status_code == 404
