from datetime import datetime

from bson import ObjectId

from app.models.cart import Cart, CartItem, AddProductCart, CreateCart
from app.db.collections import carts_collection, cart_items_collection
from app.schemas.cart import cart_item_schema


class CartService:

    @staticmethod
    async def add_product_to_cart(product: AddProductCart, user_id: str) -> list[CartItem]:
        cart_exists = await CartService.cart_exists(user_id)

        if cart_exists:
            pass
        else:
            cart_id = await CartService.create_cart(user_id)
            cart_item = await CartService.create_cart_item(product, cart_id)

            print("cart_item ===>", cart_item)

            return [cart_item]

        # Check if the user has a Cart,
        #
        # if not, create a Cart
        # Get the Cart ID
        # Create a cart item using the CartId and UserId
        #
        # If cart is present, check if product is in the cart, if it is, update it my the quantity
        # If product is not present, add the product
        # Then update the main product quantity

    @staticmethod
    async def cart_exists(user_id: str) -> bool:
        return carts_collection.find_one({"user_id": user_id}) is not None

    @staticmethod
    async def create_cart(user_id: str) -> str:
        cart = carts_collection.insert_one(
            {
                "user_id": user_id,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )

        return cart.inserted_id

    @staticmethod
    async def create_cart_item(product: AddProductCart, cart_id: str) -> CartItem:
        product_obj = product.model_dump()
        product_obj.update({"cart_id": cart_id})

        cart_item = cart_items_collection.insert_one(product_obj)

        product_obj.update({"_id": cart_item.inserted_id})

        print("product_obj ===>", product_obj)

        return cart_item_schema(product_obj)
