from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.product import ProductOut, ProductCreate, ProductUpdate
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductOut])
def list_all_products(db: Session = Depends(get_db)):
    return product_service.list_products(db)

@router.get("/{product_id}", response_model=ProductOut)
def get_single_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, product_id)

@router.post("/", response_model=ProductOut, status_code=201)
def create_new_product(data: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, data)

@router.put("/{product_id}", response_model=ProductOut)
def update_existing_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
):
    return product_service.update_product(db, product_id, data)

@router.delete("/{product_id}")
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.delete_product(db, product_id)
