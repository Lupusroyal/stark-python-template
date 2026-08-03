from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Stark API"
    app_version: str = "0.1.0"
    app_env: str = "development"

    debug: bool = False

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/stark_db"

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    allowed_hosts: list[str] = [
        "localhost",
        "127.0.0.1",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
