# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status
# from app.db import models
# from app.schemas.user import UserCreate
# from app.core.security import get_password_hash


# def create_user(db: Session, user_data: UserCreate):
#     # Check if email already exists
#     existing = db.query(models.User).filter(models.User.email == user_data.email).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_pw = get_password_hash(user_data.password)

#     role = user_data.role if hasattr(user_data, "role") and user_data.role else "user"

#     user = models.User(
#         email=user_data.email,
#         hashed_password=hashed_pw,
#         role=role
#     )

#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from app.db import models
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def create_user(db: Session, user_data: UserCreate):
    try:
        existing = db.query(models.User).filter(models.User.email == user_data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pw = get_password_hash(user_data.password)
        role = user_data.role if hasattr(user_data, "role") and user_data.role else "user"

        user = models.User(email=user_data.email, hashed_password=hashed_pw, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error while creating user: {str(e)}")


def get_user_by_email(db: Session, email: str):
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
