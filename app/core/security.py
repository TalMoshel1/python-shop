# from passlib.context import CryptContext
# from datetime import datetime
# from jose import jwt, JWTError
# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from sqlalchemy.orm import Session
# from app.core.config import settings
# from app.db.session import get_db
# from app.db import models

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# MAX_BCRYPT_LENGTH = 72

# security = HTTPBearer()


# # --- הצפנת סיסמאות ---
# def get_password_hash(password: str) -> str:
#     password_bytes = password.encode("utf-8")
#     if len(password_bytes) > MAX_BCRYPT_LENGTH:
#         password_bytes = password_bytes[:MAX_BCRYPT_LENGTH]
#         password = password_bytes.decode("utf-8", errors="ignore")
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     password_bytes = plain_password.encode("utf-8")
#     if len(password_bytes) > MAX_BCRYPT_LENGTH:
#         password_bytes = password_bytes[:MAX_BCRYPT_LENGTH]
#         plain_password = password_bytes.decode("utf-8", errors="ignore")
#     return pwd_context.verify(plain_password, hashed_password)


# # --- אימות JWT ---

# def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
#     """בודקת JWT ומחזירה את המשתמש המחובר"""
#     token = credentials.credentials  
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if user is None:
#         raise credentials_exception

#     return user

# def require_admin(current_user: models.User = Depends(get_current_user)):
#     """בודקת אם המשתמש המחובר הוא אדמין"""
#     if current_user.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You must be an admin to perform this action",
#         )
#     return current_user


from passlib.context import CryptContext
from datetime import datetime
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.db import models

# --- הגדרות הצפנה ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_LENGTH = 72

def get_password_hash(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > MAX_BCRYPT_LENGTH:
        password_bytes = password_bytes[:MAX_BCRYPT_LENGTH]
        password = password_bytes.decode("utf-8", errors="ignore")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")
    if len(password_bytes) > MAX_BCRYPT_LENGTH:
        password_bytes = password_bytes[:MAX_BCRYPT_LENGTH]
        plain_password = password_bytes.decode("utf-8", errors="ignore")
    return pwd_context.verify(plain_password, hashed_password)


# --- אימות עם Bearer Token בלבד ---
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    בודקת JWT ומחזירה את המשתמש המחובר על סמך ה־Bearer token בלבד
    """
    token = credentials.credentials  # קבלת ה־token מתוך ה־Authorization header

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


def require_admin(current_user: models.User = Depends(get_current_user)):
    """
    בודקת אם המשתמש המחובר הוא אדמין
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be an admin to perform this action",
        )
    return current_user
