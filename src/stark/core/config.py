from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Stark API"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
