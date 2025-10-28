# from datetime import datetime, timedelta
# from jose import jwt
# from fastapi import HTTPException, status
# from sqlalchemy.orm import Session
# from app.core.config import settings
# from app.core.security import verify_password
# from app.services.user_service import get_user_by_email
# from app.db import models


# # JWT config
# SECRET_KEY = settings.JWT_SECRET_KEY
# ALGORITHM = settings.JWT_ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = 120  # 2 hours


# def authenticate_user(db: Session, email: str, password: str):
#     """
#     Verify that the given email/password are valid.
#     """
#     user = get_user_by_email(db, email)
#     if not user or not verify_password(password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials"
#         )
#     return user


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     """
#     Generate a signed JWT token with optional expiration.
#     """
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def login(db: Session, email: str, password: str) -> str:
#     """
#     Authenticate the user and return a JWT token.
#     """
#     user = authenticate_user(db, email, password)

#     payload = {
#         "sub": str(user.id),
#         "email": user.email,
#         "role": user.role,
#         "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
#     }

#     token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#     return token


from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.security import verify_password
from app.services.user_service import get_user_by_email
from app.db import models


ACCESS_TOKEN_EXPIRE_MINUTES = 120
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM


def authenticate_user(db: Session, email: str, password: str):
    """
    Verify user's credentials.
    """
    try:
        user = get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create JWT access token.
    """
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token generation failed: {str(e)}")


def login(db: Session, email: str, password: str) -> str:
    """
    Authenticate a user and return a JWT token.
    """
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during login: {str(e)}")
