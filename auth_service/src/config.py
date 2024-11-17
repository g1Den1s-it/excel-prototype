from pydantic import Field
from pydantic_settings import BaseSettings


class JWTTokenConfig(BaseSettings):
    JWT_ALG: str = Field(default="HS256")
    JWT_SECRET: str = Field(default='')
    ACCESS_TOKEN_EXPIRE_MIN: int = Field(default=120)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    class Config:
        env_file = ".env"
        extra = "ignore"

jwt_token_config = JWTTokenConfig()