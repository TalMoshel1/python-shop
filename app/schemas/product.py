from pydantic import BaseModel, Field, PositiveInt, condecimal

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    price: condecimal(gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    price: condecimal(gt=0, max_digits=10, decimal_places=2) | None = None
    stock: int | None = Field(None, ge=0)

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
