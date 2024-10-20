from fastapi import HTTPException
from starlette import status
from bson import ObjectId
from app.db.collections import products_collection
from app.schemas.product import all_product_data, product_data
from app.models.product import Product, CreateProduct, UpdateProduct
from datetime import datetime

class ProductService:

    @staticmethod
    async def get_all_products() -> list[Product]:
        products = products_collection.find()
        return all_product_data(products)

    @staticmethod
    async def create_product(product: CreateProduct) -> Product:
        new_product = product.model_dump()
        new_product['price'] = float(new_product['price'])
        new_product['status'] = new_product['status'].value
        new_product['category'] = new_product['category'].value
        new_product["image_url"] = str(new_product["image_url"])
        new_product['created_at'] = datetime.now()
        new_product['updated_at'] = datetime.now()

        response = products_collection.insert_one(new_product)
        new_product['_id'] = response.inserted_id

        return product_data(new_product)

    @staticmethod
    async def get_product(product_id: str) -> Product:
        product_id_obj = ObjectId(product_id)
        product = products_collection.find_one({"_id": product_id_obj })
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with product id '{product_id}' was not found")
        return product_data(product)

    @staticmethod
    async def update_product(product_id: str, updated_product: UpdateProduct) -> Product:
        product_id_obj = ObjectId(product_id)
        product = await ProductService.get_product(product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with product id '{product_id}' was not found")

        updated_product_obj = updated_product.model_dump(exclude_unset=True)
        updated_product_obj['updated_at'] = datetime.now()

        response = products_collection.update_one({"_id": product_id_obj}, {"$set": updated_product_obj})

        if response.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with product id '{product_id}' was not updated")

        return await ProductService.get_product(product_id)

    @staticmethod
    async def delete_product(product_id: str) -> None:
        product_id_obj = ObjectId(product_id)
        product = await ProductService.get_product(product_id)

        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with product id '{product_id}' does not exist")

        response = products_collection.delete_one({"_id": product_id_obj})

        if response.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with product id '{product_id}' was not deleted")

        return None
