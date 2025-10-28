# from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
# from sqlalchemy.orm import relationship
# import enum
# from datetime import datetime

# from app.db.base import Base  

# class OrderStatus(str, enum.Enum):
#     pending = "pending"
#     paid = "paid"
#     cancelled = "cancelled"


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     role = Column(String, default="user")
#     orders = relationship("Order", back_populates="user")


# class Product(Base):
#     __tablename__ = "products"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#     price = Column(Float, nullable=False)
#     stock = Column(Integer, nullable=False)
#     currency = Column(String, default="USD")


# class Order(Base):
#     __tablename__ = "orders"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
#     status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())  
#     user = relationship("User", back_populates="orders")
#     items = relationship("OrderItem", back_populates="order", cascade="all, delete")


# class OrderItem(Base):
#     __tablename__ = "order_items"
#     id = Column(Integer, primary_key=True)
#     order_id = Column(Integer, ForeignKey("orders.id"))
#     product_id = Column(Integer, ForeignKey("products.id"))
#     quantity = Column(Integer, nullable=False)
#     unit_price = Column(Float, nullable=False)
#     order = relationship("Order", back_populates="items")
#     product = relationship("Product")


from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, DateTime, func
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from app.db.base import Base


class OrderStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    currency = Column(String, default="USD")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # ✅ fixed import
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
