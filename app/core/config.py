import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    ADMIN_EMAIL_EXTENSION: str = os.getenv("ADMIN_EMAIL_EXTENSION")
    REFRESH_TOKEN_EXPIRY: int = os.getenv("REFRESH_TOKEN_EXPIRY")
    ACCESS_TOKEN_EXPIRY: int = os.getenv("ACCESS_TOKEN_EXPIRY")


settings = Settings()
