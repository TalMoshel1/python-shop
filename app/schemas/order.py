from pydantic import BaseModel, Field, PositiveInt, condecimal
from typing import List
from datetime import datetime


class OrderItemRequest(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt


class OrderCreateRequest(BaseModel):
    items: List[OrderItemRequest] = Field(..., min_items=1)


class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    unit_price: condecimal(gt=0, max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True
