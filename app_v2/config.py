import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    title: str = "Drag Queens Collection API - v2"
    description: str = """This is a Drag Queens Collection API documentation based on the OpenApi
                       specification. Main goal of the project is to create simple database
                       available for everybody."""
    version: str = "2.0"

    deta_project_key: str = os.environ.get("DETA_PROJECT_KEY")
    jwt_algorithm: str = os.environ.get("ALGORITHM")
    jwt_secret: str = os.environ.get("JWT_SECRET")
    jwt_expiry_minutes: int = int(os.environ.get("JWT_EXPIRY_MINUTES", 5))
    jwt_expiry_hours: int = int(os.environ.get("JWT_EXPIRY_HOURS", 1))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
