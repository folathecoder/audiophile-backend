from fastapi import FastAPI
from app.core.logger import setup_logging
from app.db.mongodb import client
from app.api.v1.endpoints.auth import auth_router
from app.api.v1.endpoints.product import product_router
import logging
from contextlib import asynccontextmanager

# Setup logging configuration
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        client.admin.command('ping')
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
    lifespan=lifespan
)

app.include_router(auth_router, prefix=f"{base_url}/auth", tags=["Auth"])
app.include_router(product_router, prefix=f"{base_url}/products", tags=["Product"])
