# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.db.session import get_db
# from app.schemas.order import OrderCreateRequest, OrderOut
# from app.services import order_service
# from app.core.security import get_current_user, require_admin
# from app.db import models

# router = APIRouter(prefix="/orders", tags=["Orders"])


# @router.post("/", response_model=OrderOut, status_code=201)
# def create_order(
#     order_req: OrderCreateRequest,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     """
#     ✅ Only logged-in users can create orders.
#     - The stock is decreased automatically in order_service.
#     - No need to use PUT /products.
#     """
#     return order_service.create_order(db, order_req)


# @router.get("/{order_id}", response_model=OrderOut)
# def get_order(
#     order_id: int,
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user),
# ):
#     """
#     ✅ Only the user who owns the order (or admin) can view it.
#     """
#     order = order_service.get_order(db, order_id)

#     if current_user.role != "admin" and order.user_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You are not authorized to view this order.",
#         )

#     return order


# @router.get("/", response_model=list[OrderOut], dependencies=[Depends(require_admin)])
# def list_all_orders(db: Session = Depends(get_db)):
#     """
#     ✅ Only admins can view all orders.
#     """
#     return db.query(models.Order).all()

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.order import OrderCreateRequest, OrderOut
from app.services import order_service
from app.core.security import get_current_user, require_admin

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut, status_code=201)
def create_order(
    order_req: OrderCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Create a new order (status = pending)."""
    return order_service.create_order(db, order_req, current_user)


@router.get("/my", response_model=List[OrderOut])
def list_my_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """List all orders of the logged-in user (paginated)."""
    return order_service.list_my_orders(db, current_user, skip=skip, limit=limit)




@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Fetch a single order by ID (only if belongs to current user or admin)."""
    return order_service.get_order(db, order_id, current_user)


@router.get("/admin/all", response_model=List[OrderOut], dependencies=[Depends(require_admin)])
def list_all_orders_admin(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """List all orders in the system (admin only, paginated)."""
    return order_service.list_all_orders_admin(db, skip=skip, limit=limit)
