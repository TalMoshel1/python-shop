from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db import models
from app.schemas.order import OrderCreateRequest
from app.core.exceptions import BusinessError



def create_order(db: Session, order_req: OrderCreateRequest):
    """
    1. מאמת שיש מלאי לכל המוצרים
    2. מוריד מלאי
    3. יוצר order + order_items
    הכל כחלק מטרנזקציה אחת
    """
    # נעבוד ידנית עם טרנזקציה כדי לוודא עקביות
    try:
        order = models.Order()
        db.add(order)
        db.flush()  # מקבל order.id לפני commit

        for item in order_req.items:
            product = (
                db.query(models.Product)
                .filter(models.Product.id == item.product_id)
                .with_for_update()  # נועל את השורה (בפוסטגרס)
                .first()
            )

            if not product:
                raise BusinessError(f"Product {item.product_id} does not exist", status_code=404)

            if product.stock < item.quantity:
                raise BusinessError(f"Not enough stock for product {product.id}", status_code=400)

            # עדכן מלאי
            product.stock -= item.quantity

            order_item = models.OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
            )
            db.add(order_item)

        db.commit()
        db.refresh(order)

        # טען מחדש עם פריטים
        db.refresh(order)
        # lazy load items with explicit query
        order.items  # access to ensure relationship is loaded

        return order
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order",
        ) from e


def get_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    # load items (simple access triggers relationship)
    order.items
    return order
