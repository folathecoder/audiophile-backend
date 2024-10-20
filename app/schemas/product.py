def product_data(product):
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "stock_quantity": product["stock_quantity"],
        "status": product["status"],
        "category": product["category"],
        "image_url": product["image_url"],
        "created_at": product["created_at"],
        "updated_at": product["updated_at"]
    }

def all_product_data(products):
    return [product_data(product) for product in products]