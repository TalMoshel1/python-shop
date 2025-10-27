from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.order import OrderCreateRequest, OrderOut
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut, status_code=201)
def create_order(order_req: OrderCreateRequest, db: Session = Depends(get_db)):
    return order_service.create_order(db, order_req)

@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return order_service.get_order(db, order_id)
