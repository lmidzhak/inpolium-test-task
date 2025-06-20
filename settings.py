from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Blog Management API"

    DATABASE_URL: str | None = "sqlite+aiosqlite:///./blog.db"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
