from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db import models
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def create_user(db: Session, user_data: UserCreate):
    existing = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user_data.password)
    user = models.User(email=user_data.email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
