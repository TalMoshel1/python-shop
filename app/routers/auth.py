from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import LoginRequest, TokenResponse
from app.services import user_service, auth_service


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut, status_code=201)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, data)
    return user

@router.post("/login", response_model=TokenResponse)
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    token = auth_service.login(db, data.email, data.password)
    return {"access_token": token, "token_type": "bearer"}
