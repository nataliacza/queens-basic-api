import datetime
import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    title: str = "Drag Queens Collection API"
    description: str = """Drag Queens Collection API is an application, using which 
    you can search for information about Drag Queens in Poland. Main goal 
    of the project is to create lightweight and simple db available for everybody."""
    version: str = os.environ.get("PROJECT_VERSION", "0.0.0")

    deta_project_key: str = os.environ.get("DETA_PROJECT_KEY", "no-key")

    token_algorithm: str = os.environ.get("TOKEN_ALGORITHM", "no-algorithm")
    token_type: str = os.environ.get("TOKEN_TYPE", "no-type")
    token_issuer: str = os.environ.get("TOKEN_ISSUER", "no-issuer")
    jwt_secret: str = os.environ.get("JWT_SECRET", "no-secret")
    jwt_expiry_minutes: int = int(os.environ.get("JWT_EXPIRY_MINUTES", 5))
    jwt_expiry_hours: int = int(os.environ.get("JWT_EXPIRY_HOURS", 1))

    db_limit: int = int(os.environ.get("DATABASE_LIMIT", 5))
    db_item_expire_at = datetime.datetime.fromisoformat("2023-10-01T00:00:00")

    cors_origins: list = list(os.environ.get("ORIGINS", []))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
