from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    ALPHAVANTAGE_URL: str = "https://www.alphavantage.co"
    ALPHAVANTAGE_API_KEY: str = "demo"
    DATABASE_URL: str = ""
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env")

config = Config()

