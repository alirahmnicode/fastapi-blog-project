from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class Settings(BaseSettings):
    JWT_SECRET_KEY: str = secrets.token_hex(32)
    USE_CREDENTIALS: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
