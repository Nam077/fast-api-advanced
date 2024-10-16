from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Class-Based App"
    DATABASE_URL: str = "sqlite:///./test.db"
    MASTER_KEY: str = "master_key"
    class Config:
        env_file = ".env"

settings = Settings()
