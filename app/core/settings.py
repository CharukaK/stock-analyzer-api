from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ALPHAVANTAGE_URL: str = "https://www.alphavantage.co"
    ALPHAVANTAGE_API_KEY: str = ""
    DATABASE_URL: str = ""
    DEBUG: bool = False

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(env_file=".env")

settings = Settings()

