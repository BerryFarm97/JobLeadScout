import pytest

from unittest.mock import Mock
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_lifespan_initializes_database(monkeypatch):
    mock_init_db = Mock(return_value=True)

    monkeypatch.setattr("app.main.init_db", mock_init_db)

    with TestClient(app):
        pass

    mock_init_db.assert_called_once_with()


def test_lifespan_fails_to_initialize_database(monkeypatch):
    mock_init_db_failed = Mock(return_value=False)

    monkeypatch.setattr("app.main.init_db", mock_init_db_failed)

    with pytest.raises(RuntimeError, match="Failed to initialize database"):
        with TestClient(app):
            pass

    mock_init_db_failed.assert_called_once_with()