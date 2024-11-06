import os
from pydantic_settings import BaseSettings


class JWTTokenConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MIN: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    class Config:
        env_file = ".env"
        extra = "ignore"

jwt_token_config = JWTTokenConfig()