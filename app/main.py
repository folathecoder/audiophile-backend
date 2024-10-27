from fastapi import FastAPI
from app.db.mongodb import client
from app.api.v1.endpoints.auth import auth_router
from app.api.v1.endpoints.product import product_router
from app.api.v1.endpoints.user import user_router
from app.api.v1.endpoints.cart import cart_router
from app.core.logger import logger
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        client.admin.command("ping")
        logger.info("Application successfully connected to MongoDB!")
        logger.info(f"Starting application...")

        yield

    except Exception as e:
        logger.error("Application failed to connect to MongoDB: %s", e)
        raise

    finally:
        logger.info("Shutting down application...")
        await client.close()


version = "v1"
base_url = f"/api/{version}"

app = FastAPI(
    title="Audiophile",
    description="An eCommerce application backend",
    version=version,
    lifespan=lifespan,
)

app.include_router(auth_router, prefix=f"{base_url}/auth", tags=["Auth"])
app.include_router(user_router, prefix=f"{base_url}/user", tags=["User"])
app.include_router(product_router, prefix=f"{base_url}/products", tags=["Product"])
app.include_router(cart_router, prefix=f"{base_url}/cart", tags=["Cart"])
