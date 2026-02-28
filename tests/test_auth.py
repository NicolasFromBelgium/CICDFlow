from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_register_and_login_success():
    """TDD - Register puis login doit marcher"""
    # Register
    response = client.post("/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200

    # Login
    response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_fail():
    """TDD - Mauvais mot de passe = 401"""
    response = client.post("/login", data={"username": "testuser", "password": "wrong"})
    assert response.status_code == 401
