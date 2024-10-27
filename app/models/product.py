from pydantic import BaseModel, Field, confloat
from datetime import datetime
from enum import Enum
from typing import Optional
from app.utils.regex import https_url_regex


class ProductCategory(str, Enum):
    HEADPHONES = "Headphones"
    SPEAKERS = "Speakers"
    EARPHONES = "Earphones"


class ProductStatus(str, Enum):
    IN_STOCK = "In stock"
    OUT_OF_STOCK = "Out of stock"


class ProductBaseModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=20)
    price: confloat(gt=0)
    stock_quantity: int = Field(..., ge=0)
    status: ProductStatus = Field(default=ProductStatus.IN_STOCK)
    category: ProductCategory
    image_url: str = Field(
        ...,
        pattern=https_url_regex,
    )


class Product(ProductBaseModel):
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CreateProduct(ProductBaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UpdateProduct(ProductBaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=20)
    price: Optional[confloat(gt=0)] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    status: Optional[ProductStatus] = None
    category: Optional[ProductCategory] = None
    image_url: Optional[str] = Field(
        None,
        pattern=https_url_regex,
    )
