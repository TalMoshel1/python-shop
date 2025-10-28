from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: float
    currency: str = Field(default="USD", pattern="^(USD|ILS|EUR)$")  # ✅ רק דולר, שקל או יורו
    stock: Optional[int] = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    currency: Optional[str] = Field(default=None, pattern="^(USD|ILS|EUR)$")
    stock: Optional[int]

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
