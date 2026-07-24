from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Stark API"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = True
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/stark_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
