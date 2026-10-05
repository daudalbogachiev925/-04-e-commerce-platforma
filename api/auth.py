from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os
from db import get_session
from models import User

router = APIRouter()
SECRET = os.getenv("SECRET_KEY", "change-me")

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None

class LoginIn(BaseModel):
    email: EmailStr
    password: str

def make_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, SECRET, algorithm="HS256")

@router.post("/register")
def register(data: RegisterIn, db=Depends(get_session)):
    if db.query(User).filter_by(email=data.email).first():
        raise HTTPException(400, "Email уже занят")
    u = User(email=data.email, password_hash=bcrypt.hash(data.password), name=data.name)
    db.add(u); db.commit(); db.refresh(u)
    return {"id": u.id, "token": make_token(u.id)}

@router.post("/login")
def login(data: LoginIn, db=Depends(get_session)):
    u = db.query(User).filter_by(email=data.email).first()
    if not u or not bcrypt.verify(data.password, u.password_hash):
        raise HTTPException(401, "Неверные данные")
    return {"token": make_token(u.id)}
