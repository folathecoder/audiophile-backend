from app.db.mongodb import db

products_collection = db["products"]
users_collection = db["users"]
carts_collection = db["carts"]
cart_items_collection = db["cart_items"]
