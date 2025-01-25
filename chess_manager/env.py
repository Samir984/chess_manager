from typing import Optional

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Environment(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DEBUG: bool = True
    DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost:5432/smurfskins"
    )
    


   

ENV = Environment()