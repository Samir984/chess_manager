from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Environment(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DEBUG: bool = True
    DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost:5432/smurfskins"
    )
    SECRET_KEY: str = "your-secret"
    CLOUD_NAME: str = "cloud_name"
    API_KEY: str = "cloud_api_key"
    API_SECRET: str = "cloud_api_secret"


ENV = Environment()
print(ENV)
