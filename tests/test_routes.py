import pytest
from fastapi.testclient import TestClient
from http import HTTPStatus

def test_root_endpoint(test_client: TestClient):
    """
    Test the root endpoint returns the expected welcome message
    """
    response = test_client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert "message" in response.json()
    assert response.json()["message"] == "Welcome to FastAPI Boilerplate"

def test_health_check(test_client: TestClient):
    """
    Test the health check endpoint returns OK status
    """
    response = test_client.get("/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "OK"}

def test_nonexistent_endpoint(test_client: TestClient):
    """
    Test that accessing a non-existent endpoint returns 404
    """
    response = test_client.get("/nonexistent")
    assert response.status_code == HTTPStatus.NOT_FOUND 