from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    JWT_SECRET_KEY: str = "test"
    USE_CREDENTIALS: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
