from fastapi import APIRouter, HTTPException, Depends
from app.models.product import (
    Product,
    CreateProduct,
    UpdateProduct,
    ProductCategory,
    ProductStatus,
)
from app.services.product_service import ProductService
from starlette import status
from app.auth.bearer_auth import AccessTokenBearer

product_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@product_router.get("/", status_code=status.HTTP_200_OK, response_model=list[Product])
async def get_all_products(access=Depends(access_token_bearer)):
    try:
        print("access", access)
        return await ProductService.get_all_products()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No product was found: {str(e)}",
        )


@product_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Product)
async def create_product(product: CreateProduct, access=Depends(access_token_bearer)):
    try:
        return await ProductService.create_product(product)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product was not created: {str(e)}",
        )


@product_router.get(
    "/{product_id}", status_code=status.HTTP_200_OK, response_model=Product
)
async def get_product(product_id: str, access=Depends(access_token_bearer)):
    try:
        return await ProductService.get_product(product_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with product id '{product_id}' was not found: {str(e)}",
        )


@product_router.patch(
    "/{product_id}", status_code=status.HTTP_200_OK, response_model=Product
)
async def update_product(
    product_id: str, updated_product: UpdateProduct, access=Depends(access_token_bearer)
):
    try:
        return await ProductService.update_product(product_id, updated_product)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with product id '{product_id}' was not updated: {str(e)}",
        )


@product_router.delete(
    "/{product_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_product(product_id: str, access=Depends(access_token_bearer)):
    try:
        return await ProductService.delete_product(product_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with product id '{product_id}' was not deleted: {str(e)}",
        )


@product_router.get(
    "/category/{category_name}",
    status_code=status.HTTP_200_OK,
    response_model=list[Product],
)
async def get_products_by_category(
    category_name: ProductCategory, access=Depends(access_token_bearer)
):
    try:
        print("access ===>", access)
        return await ProductService.get_products_by_category(category_name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Products in '{category_name}' category could not be fetched: {str(e)}",
        )


@product_router.get(
    "/status/{status_name}",
    status_code=status.HTTP_200_OK,
    response_model=list[Product],
)
async def get_products_by_status(
    status_name: ProductStatus, access=Depends(access_token_bearer)
):
    try:
        return await ProductService.get_products_by_status(status_name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Products with {status} status could not be fetched: {str(e)}",
        )
