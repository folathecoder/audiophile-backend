from datetime import datetime
from pydantic import BaseModel, Field


class CartBaseModel(BaseModel):
    user_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Cart(CartBaseModel):
    cart_id: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CreateCart(CartBaseModel):
    pass


class CartItemBaseModel(BaseModel):
    product_id: str
    quantity: int = Field(..., ge=0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class CartItem(CartItemBaseModel):
    cart_item_id: str
    cart_id: str


class AddProductCart(CartItemBaseModel):
    pass
