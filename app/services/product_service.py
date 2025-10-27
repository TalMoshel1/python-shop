from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db import models
from app.schemas.product import ProductCreate, ProductUpdate


def list_products(db: Session):
    return db.query(models.Product).all()


def get_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


def create_product(db: Session, data: ProductCreate):
    # enforce unique name
    existing = db.query(models.Product).filter(models.Product.name == data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with that name already exists",
        )

    product = models.Product(
        name=data.name,
        price=data.price,
        stock=data.stock,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, data: ProductUpdate):
    product = get_product(db, product_id)

    if data.name is not None:
        product.name = data.name
    if data.price is not None:
        product.price = data.price
    if data.stock is not None:
        product.stock = data.stock

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
    return {"deleted": True}
