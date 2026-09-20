"""Black-box integration test for the running Docker Compose stack.

Unlike test_agent_relay.py, this test does not import the app or touch the
database directly, and it never resets tables: it only speaks HTTP to
whatever is listening at RELAY_BASE_URL, so it is safe to run against the
live `api` service backed by the compose stack's real PostgreSQL database.
"""

from __future__ import annotations

import os

import httpx


def register(client: httpx.Client, name: str) -> tuple[dict, dict[str, str]]:
    response = client.post("/api/v1/agents", json={"name": name})
    assert response.status_code == 201
    data = response.json()
    return data, {"Authorization": f"Bearer {data['token']}"}


def test_scenario_1_against_running_compose_stack():
    base_url = os.environ.get("RELAY_BASE_URL", "http://127.0.0.1:8000")
    with httpx.Client(base_url=base_url, timeout=10) as client:
        assert client.get("/health").json() == {"status": "ok"}
        assert client.get("/ready").json() == {"status": "ready"}

        sender, sender_headers = register(client, "compose-test-sender")
        recipient, recipient_headers = register(client, "compose-test-recipient")

        sent = client.post(
            "/api/v1/tasks",
            headers=sender_headers,
            json={"to": recipient["agent_id"], "input": "Please review the compose stack"},
        )
        assert sent.status_code == 201
        assert sent.json()["status"] == "queued"
        task_id = sent.json()["task_id"]

        claim = client.post(
            "/api/v1/tasks/claim",
            headers=recipient_headers,
            json={"worker_id": "compose-test-worker", "wait_seconds": 0},
        )
        assert claim.status_code == 200
        claim_data = claim.json()
        assert claim_data["task_id"] == task_id
        assert claim_data["from"] == sender["agent_id"]

        complete = client.post(
            f"/api/v1/tasks/{task_id}/complete",
            headers=recipient_headers,
            json={"claim_token": claim_data["claim_token"], "output": "Reviewed: PostgreSQL-backed stack works"},
        )
        assert complete.status_code == 200
        assert complete.json() == {"task_id": task_id, "status": "completed"}

        result = client.get(f"/api/v1/tasks/{task_id}", headers=sender_headers)
        assert result.status_code == 200
        body = result.json()
        assert body["status"] == "completed"
        assert body["output"] == "Reviewed: PostgreSQL-backed stack works"
        assert body["error"] is None

        attempts = client.get(f"/api/v1/tasks/{task_id}/attempts", headers=sender_headers).json()
        assert attempts["items"][0]["outcome"] == "completed"
        assert attempts["items"][0]["worker_id"] == "compose-test-worker"

        print(f"task_id={task_id} sender_token={sender['token']}")
