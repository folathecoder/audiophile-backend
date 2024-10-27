def cart_item_schema(cart_item):
    return {
        "cart_item_id": str(cart_item["_id"]),
        "cart_id": cart_item["cart_id"],
        "product_id": cart_item["product_id"],
        "quantity": cart_item["quantity"],
        "created_at": cart_item["created_at"],
        "updated_at": cart_item["updated_at"],
    }
