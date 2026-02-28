from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    """TDD - Test rouge puis vert : login valide doit retourner token"""
    response = client.post("/login", json={"username": "test45", "password": "test"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_fail():
    """TDD - Mauvais identifiants doit renvoyer 401"""
    response = client.post("/login", json={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides"
