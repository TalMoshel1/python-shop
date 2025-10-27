# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     APP_NAME: str = "Shop API"
#     ENV: str = "development"

#     JWT_SECRET: str
#     JWT_ALGORITHM: str = "HS256"

#     DB_URL: str = "sqlite:///./shop.db"
#     LOG_LEVEL: str = "info"

#     class Config:
#         env_file = ".env"

# settings = Settings()

# def get_settings() -> Settings:
#     """Provide Settings instance for dependency injection."""
#     return settings


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Shop API"
    ENV: str = "local"
    LOG_LEVEL: str = "info"

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    DB_URL: str = "sqlite:///./shop.db"

    class Config:
        env_file = ".env"


settings = Settings()


def get_settings() -> Settings:
    """Return current app settings."""
    return settings
