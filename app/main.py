from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.testclient import TestClient

app = FastAPI(
    title="CICDFlow - Login Sécurisé",
    description="Projet TDD + DevOps CI/CD complet",
    version="0.1.0"
)

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur CICDFlow - Page d'accueil + Login sécurisé (TDD + CI/CD)"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "env": "dev"}

#@app.post("/login")
#def login(request: LoginRequest):
    # Fake auth pour premier TDD (on passera à fastapi-users + JWT + DB après)
 #   if request.username == "test" and request.password == "test":
  #      return {"access_token": "fake-jwt-token-12345", "token_type": "bearer"}
   # raise HTTPException(status_code=401, detail="Identifiants invalides")
