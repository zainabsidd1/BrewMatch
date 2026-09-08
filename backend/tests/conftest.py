"""Isolated SQLite setup. DATABASE_URL is forced before app imports so tests
never use the Postgres instance from .env."""

from __future__ import annotations

import os
import sys
from collections.abc import Callable, Generator
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite://"

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import database

TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
database.engine = TEST_ENGINE
database.SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=TEST_ENGINE,
)

from database import Base, get_db  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402
import models  # noqa: E402, F401
import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _never_call_real_ollama(monkeypatch: pytest.MonkeyPatch) -> None:
    def _unavailable() -> bool:
        return False

    def _blocked(*_args, **_kwargs) -> str:
        raise AssertionError("Tests must not call the real Ollama server")

    monkeypatch.setattr("ai_match._ollama_available", _unavailable)
    monkeypatch.setattr("ai_match._call_ollama", _blocked)
    monkeypatch.setattr("personalized_recs._ollama_available", _unavailable)
    monkeypatch.setattr("personalized_recs._call_ollama", _blocked)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    Base.metadata.drop_all(bind=TEST_ENGINE)
    Base.metadata.create_all(bind=TEST_ENGINE)

    def override_get_db():
        session = database.SessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture
def create_user(client: TestClient) -> Callable[..., dict]:
    def _create(
        email: str = "test@example.com",
        password: str = "Correct123!",
        name: str = "Test User",
    ) -> dict:
        response = client.post(
            "/auth/register",
            json={"email": email, "password": password, "name": name},
        )
        assert response.status_code == 201, response.text
        return response.json()

    return _create


@pytest.fixture
def auth_header(client: TestClient, create_user: Callable[..., dict]) -> Callable[..., dict[str, str]]:
    def _header(
        email: str = "test@example.com",
        password: str = "Correct123!",
        register: bool = True,
    ) -> dict[str, str]:
        if register:
            create_user(email=email, password=password)
        response = client.post(
            "/auth/login",
            json={"email": email, "password": password},
        )
        assert response.status_code == 200, response.text
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _header
