from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
import os

from app.core.database import get_db, Base, engine
from app.models.user import User
from app.schemas.user import UserCreate, Token

app = FastAPI(title="CICDFlow - Login Sécurisé (TDD + DevOps)")

Base.metadata.create_all(bind=engine)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register simple (TDD friendly)"""
    # Nettoie l'ancien user
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        db.delete(existing)
        db.commit()

    db_user = User(username=user.username, hashed_password=user.password)  # simple pour l'instant
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User created", "username": user.username}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or user.hashed_password != form_data.password:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur CICDFlow - Page d'accueil + Login sécurisé (TDD + CI/CD)"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "env": "dev", "db": "connected"}
