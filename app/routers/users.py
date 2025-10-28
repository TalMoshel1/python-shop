from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.db import models

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    """
    החזרת פרטי המשתמש המחובר
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
    }
