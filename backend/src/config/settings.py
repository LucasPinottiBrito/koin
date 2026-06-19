from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="koin backend", validation_alias="APP_NAME")
    app_env: str = Field(default="development", validation_alias=AliasChoices("APP_ENV", "ENVIRONMENT"))
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    database_url: str = Field(
        default="postgresql+psycopg://koin:koin@postgres:5432/koin",
        validation_alias="DATABASE_URL",
    )
    mongo_url: str = Field(
        default="mongodb://koin:koin@mongodb:27017/koin?authSource=admin",
        validation_alias=AliasChoices("MONGO_URL", "MONGODB_URL"),
    )
    mongo_database: str = Field(default="koin", validation_alias=AliasChoices("MONGO_DATABASE", "MONGODB_DATABASE"))
    google_client_id: str | None = Field(default=None, validation_alias="GOOGLE_CLIENT_ID")
    google_client_secret: str | None = Field(default=None, validation_alias="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str | None = Field(default=None, validation_alias="GOOGLE_REDIRECT_URI")
    openai_api_key: str | None = Field(default=None, validation_alias="OPENAI_API_KEY")
    token_encryption_key: str | None = Field(default=None, validation_alias="TOKEN_ENCRYPTION_KEY")


@lru_cache
def get_settings() -> Settings:
    return Settings()
