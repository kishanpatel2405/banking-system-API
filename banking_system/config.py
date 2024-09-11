from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Banking System"
    ENVIRONMENT: str = "development"
    BACKEND_CORS_ORIGINS: list = ["http://localhost"]
    JWT_SECRET_KEY: str = "asdfghjkl"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
