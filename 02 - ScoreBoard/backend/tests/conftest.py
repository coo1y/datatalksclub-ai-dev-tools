import os
import tempfile

# Must be set before `app.config`/`app.db.session` are imported anywhere, since the
# engine is built from this at import time. Tests run against a real (SQLite) database
# seeded by the same startup path production uses against Postgres — just a lighter
# engine, so the suite stays hermetic and fast without needing Docker.
os.environ.setdefault("DATABASE_URL", f"sqlite:///{tempfile.mkdtemp()}/test.db")

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client
