from pydantic import BaseModel, Field, condecimal, HttpUrl
from datetime import datetime
from enum import Enum
from typing import Optional

class ProductCategory(Enum):
    HEADPHONES = "Headphones"
    SPEAKERS = "Speakers"
    EARPHONES = "Earphones"

class ProductStatus(Enum):
    IN_STOCK = "In stock"
    OUT_OF_STOCK = "Out of stock"

class ProductBaseModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=20)
    price: condecimal(gt=0, decimal_places=2)
    stock_quantity: int = Field(..., ge=0)
    status: ProductStatus = Field(default=ProductStatus.IN_STOCK)
    category: ProductCategory
    image_url: HttpUrl

class Product(ProductBaseModel):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class CreateProduct(ProductBaseModel):
    pass

class UpdateProduct(ProductBaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    # description: Optional[str] = Field(None, min_length=20)
    # price: Optional[condecimal(gt=0, decimal_places=2)] = None
    # stock_quantity: Optional[int] = Field(None, ge=0)
    # status: Optional[ProductStatus] = None
    # category: Optional[ProductCategory] = None
    # image_url: Optional[HttpUrl] = None