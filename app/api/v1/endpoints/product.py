from fastapi import APIRouter, HTTPException
from app.models.product import Product, CreateProduct, UpdateProduct
from app.services.product_service import ProductService
from starlette import status

product_router = APIRouter()

@product_router.get("/", status_code=status.HTTP_200_OK, response_model=list[Product])
async def get_all_products():
    try:
        return await ProductService.get_all_products()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product was found: {str(e)}")

@product_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Product)
async def create_product(product: CreateProduct):
    try:
        return await ProductService.create_product(product)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product was not created: {str(e)}")

@product_router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=Product)
async def get_product(product_id: str):
    try:
       return await ProductService.get_product(product_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with product id '{product_id}' was not found: {str(e)}")

@product_router.patch("/{product_id}", status_code=status.HTTP_200_OK, response_model=Product)
async def update_product(product_id: str, updated_product: UpdateProduct):
    try:
        return await ProductService.update_product(product_id, updated_product)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with product id '{product_id}' was not updated: {str(e)}")

@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_product(product_id: str):
    try:
        return await ProductService.delete_product(product_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with product id '{product_id}' was not deleted: {str(e)}")
