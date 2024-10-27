from fastapi import APIRouter, HTTPException, Depends
from app.models.cart import CartItem, AddProductCart
from starlette import status
from app.services.cart_service import CartService
from app.auth.check_auth import user_authorisation_check_by_id

cart_router = APIRouter()


@cart_router.post("/add/{user_id}", status_code=status.HTTP_200_OK, response_model=None)
async def add_product_to_cart(
    product: AddProductCart,
    user_id: str,
    current_user_id=Depends(user_authorisation_check_by_id),
):
    try:
        return await CartService.add_product_to_cart(product, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to add product to cart: {current_user_id}",
        )
