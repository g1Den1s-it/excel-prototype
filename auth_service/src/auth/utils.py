import datetime

from jose import jwt
from passlib.apps import custom_app_context

from src.config import jwt_token_config


class PasswordHax:
    @staticmethod
    def create_password_hash(password: str) -> str:
        return custom_app_context.hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return custom_app_context.verify(password, password_hash)


class JWTToken:
    @staticmethod
    def create_access_token( user_id: int, **kwargs) -> str:
        # "sub": "1234567890",
        # "iss": "https://your-auth-server.com",
        # "aud": "https://your-api.com",
        # "exp": 1716326400,
        # "iat": 1716273600,
        # "nbf": 1716273600,
        # "scope": "read write",
        # "roles": ["user"],
        # "jti": "unique-token-id-123"
        to_encode = {k: v for k, v in kwargs}
        to_encode["type"] = 'access'
        to_encode['sub'] = user_id

        expire = (datetime.datetime.now(datetime.UTC) +
                  datetime.timedelta(minutes=jwt_token_config.ACCESS_TOKEN_EXPIRE_MIN))

        to_encode['expire'] = expire.strftime("%Y-%m-%d %H:%M:%S")

        access_token = jwt.encode(to_encode, jwt_token_config.JWT_SECRET, jwt_token_config.JWT_ALG)

        return access_token


    @staticmethod
    def create_refresh_token(user_id: int, email: str, **kwargs) ->  str:
        to_encode = {k: v for k, v in kwargs}
        to_encode["type"] = 'refresh'
        to_encode["sub"] = user_id
        to_encode["email"] = email

        expire = (datetime.datetime.now(datetime.UTC) +
                  datetime.timedelta(minutes=jwt_token_config.REFRESH_TOKEN_EXPIRE_DAYS))

        to_encode['expire'] = expire.strftime("%Y-%m-%d %H:%M:%S")

        refresh_token = jwt.encode(to_encode, jwt_token_config.JWT_SECRET, jwt_token_config.JWT_ALG)

        return refresh_token
