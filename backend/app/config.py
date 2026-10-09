from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'AgriWater AI'
    app_env: str = 'development'
    database_url: str = 'sqlite:///./agriwater.db'
    jwt_secret: str = 'dev-secret-change-me'
    jwt_algorithm: str = 'HS256'
    jwt_expire_minutes: int = 60
    access_token_cookie_name: str = 'agriwater_access'
    allowed_origins: str = 'http://localhost:5173'
    evaporation_provider: str = 'mock'
    evaporation_model_path: str = ''
    evaporation_model_version: str = 'development'
    cors_enabled: bool = True

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
