from fastapi import APIRouter

product_router = APIRouter()

@product_router.get("/")
async def root():
    return None