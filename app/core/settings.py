from typing import ClassVar
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ALPHAVANTAGE_URL: str = "https://www.alphavantage.co"
    ALPHAVANTAGE_API_KEY: str = ""
    DATABASE_URL: str = ""
    DEBUG: bool = False

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=".env")

    @field_validator("ALPHAVANTAGE_API_KEY")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v:
            raise ValueError("ALPHAVANTAGE_API_KEY must be set")
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_db_url(cls, v: str) -> str:
        if not v:
            raise ValueError("DATABASE_URL must be set")
        return v


settings = Settings()
