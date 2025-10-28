# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status
# from app.db import models
# from app.schemas.order import OrderCreateRequest
# from app.core.exceptions import BusinessError


# def create_order(db: Session, order_req: OrderCreateRequest):
#     """
#     יצירת הזמנה חדשה:
#     1. מאמת שיש מלאי לכל המוצרים
#     2. מוריד מלאי לפי הכמות שנרכשה
#     3. יוצר רשומת Order ורשומות OrderItem
#     4. כל הפעולה נעשית כחלק מטרנזקציה אחת
#     """

#     try:
#         # צור הזמנה חדשה
#         order = models.Order()
#         db.add(order)
#         db.flush()  # כדי לקבל order.id לפני ה-commit

#         for item in order_req.items:
#             product = (
#                 db.query(models.Product)
#                 .filter(models.Product.id == item.product_id)
#                 .with_for_update()  # נועל את השורה בזמן הבדיקה (Postgres בלבד)
#                 .first()
#             )

#             if not product:
#                 raise BusinessError(
#                     f"Product {item.product_id} does not exist",
#                     status_code=status.HTTP_404_NOT_FOUND,
#                 )

#             if product.stock < item.quantity:
#                 raise BusinessError(
#                     f"Not enough stock for product {product.name} (available: {product.stock})",
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                 )

#             # 🔽 עדכן מלאי
#             product.stock -= item.quantity

#             # צור פריט הזמנה
#             order_item = models.OrderItem(
#                 order_id=order.id,
#                 product_id=product.id,
#                 quantity=item.quantity,
#                 unit_price=product.price,
#             )
#             db.add(order_item)

#         # ✅ שמור הכל בבת אחת
#         db.commit()

#         # טען מחדש את ההזמנה עם הפריטים שלה
#         db.refresh(order)
#         order.items  # גישה כדי לוודא שהיחסים נטענים

#         return order

#     except BusinessError as e:
#         db.rollback()
#         raise HTTPException(status_code=e.status_code, detail=e.message)

#     except HTTPException:
#         db.rollback()
#         raise

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Failed to create order: {str(e)}",
#         )


# def get_order(db: Session, order_id: int):
#     """
#     שליפת הזמנה לפי מזהה, כולל הפריטים שבה.
#     """
#     order = db.query(models.Order).filter(models.Order.id == order_id).first()
#     if not order:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Order not found",
#         )
#     order.items  # טוען את היחסים של ההזמנה
#     return order

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from app.db import models
from app.schemas.order import OrderCreateRequest


def create_order(db: Session, order_req: OrderCreateRequest, current_user: models.User):
    try:
        order = models.Order(user_id=current_user.id, status=models.OrderStatus.pending)
        db.add(order)
        db.flush()

        for item in order_req.items:
            product = (
                db.query(models.Product)
                .filter(models.Product.id == item.product_id)
                .with_for_update()
                .first()
            )
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            if product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")

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
        return order

    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error while creating order: {str(e)}")


def get_order(db: Session, order_id: int, current_user: models.User):
    try:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.user_id != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Access denied")

        order.items
        return order
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while fetching order: {str(e)}")


def list_my_orders(db: Session, current_user: models.User, skip: int, limit: int):
    try:
        orders = (
            db.query(models.Order)
            .filter(models.Order.user_id == current_user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return orders
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def list_all_orders_admin(db: Session, skip: int, limit: int):
    try:
        orders = db.query(models.Order).offset(skip).limit(limit).all()
        return orders
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
