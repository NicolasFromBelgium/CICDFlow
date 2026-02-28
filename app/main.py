from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os

from app.core.database import get_db, Base, engine
from app.models.user import User
from app.schemas.login import LoginRequest   # on va créer ça juste après

app = FastAPI(title="CICDFlow - Login Sécurisé")

# Création tables au démarrage (pour dev)
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/register")
def register(user: dict, db: Session = Depends(get_db)):  # on simplifie pour TDD
    # Pour l'instant on accepte n'importe quel user (on raffinera après)
    hashed = pwd_context.hash(user["password"])
    db_user = User(username=user["username"], hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User created"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur CICDFlow - Login sécurisé (TDD + CI/CD + PostgreSQL)"}
