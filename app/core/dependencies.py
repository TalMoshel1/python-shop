from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user
from app.db.models import User

def require_admin(current_user: User = Depends(get_current_user)):
    """מאשרת רק למשתמשים עם תפקיד admin"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be an admin to perform this action",
        )
    return current_user
