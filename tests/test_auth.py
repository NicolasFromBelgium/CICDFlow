from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine
from app.models.user import User   # ← CRITIQUE : ceci enregistre la table "users"

client = TestClient(app)

# Création de la table UNE SEULE FOIS au chargement du module de test
Base.metadata.create_all(bind=engine)

def test_register_and_login_success():
    """TDD - Register puis login"""
    response = client.post("/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200

    response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fail():
    """TDD - Mauvais password = 401"""
    response = client.post("/login", data={"username": "testuser", "password": "wrong"})
    assert response.status_code == 401
