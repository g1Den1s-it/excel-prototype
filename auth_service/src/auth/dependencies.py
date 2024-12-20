from typing import Annotated

from fastapi import Header
from fastapi.params import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import service
from src.database import get_db_session
from src.auth.schemas import (
    UserSchemas,
    TokenSchemas,
    ValidResponseSchemas)
from src.auth.exceptions import (
    CreateUserException,
    FieldRequiredException,
    InvalidEmailException,
    InvalidPasswordException,
    NotCreatedTokensError,
    NotAuthorizationException,
    InvalidToken,
    NotUpdateUserError,
    NotRefreshToken)
from src.auth.service import (get_user_by_email)
from src.auth.utils import PasswordHax, JWTToken


def check_authorization(authorization: str = Header(None)) -> bool:
    if not authorization:
        raise NotAuthorizationException()

    if not authorization.startswith("Bearer "):
        raise InvalidToken()

    if not JWTToken.is_valid_token(authorization.split(" ")[1]):
        raise InvalidToken()

    return True

# create
async def valid_create_user(user_data: UserSchemas,
                      db: Annotated[AsyncSession, Depends(get_db_session)]) -> UserSchemas:
    user = await service.create_user(user_data, db)
    if not user:
        raise CreateUserException()
    return user


async def valid_login(user_data: UserSchemas,
                      db: Annotated[AsyncSession, Depends(get_db_session)]) -> TokenSchemas:
    if not user_data.email or not user_data.password:
        raise FieldRequiredException("'Email' and 'Password' are required!")

    user: UserSchemas | None = await get_user_by_email(user_data.email, db)

    if not user:
        raise InvalidEmailException()

    if not user_data.password or not user.password:
        raise InvalidPasswordException()

    if not PasswordHax.verify_password(user_data.password, user.password):
        raise InvalidPasswordException()

    if not user.email:
        raise FieldRequiredException("'Email' is required!")

    if not user.id:
        raise FieldRequiredException("'Id' is required!")

    tokens = TokenSchemas(
        access_token=JWTToken.create_access_token(user.id),
        refresh_token=JWTToken.create_refresh_token(user.id, user.email)
    )

    if not tokens.access_token and not tokens.refresh_token:
        raise NotCreatedTokensError()

    return tokens


async def valid_new_data(new_user_data: UserSchemas,
                        db: Annotated[AsyncSession, Depends(get_db_session)],
                        authorization: str = Header(None)) -> UserSchemas:

    check_authorization(authorization)

    user_payload = JWTToken.get_payload(authorization.split(" ")[1])

    if not user_payload:
        raise InvalidToken()

    user = await service.update_user(int(user_payload["sub"]),new_user_data, db)

    if not user:
        raise NotUpdateUserError()

    return user


async def valid_token(token: TokenSchemas) -> dict[str, ValidResponseSchemas]:
    valid_dict = {}

    for key, value in token.__dict__.items():
        if value is not None:
            is_valid = JWTToken.is_valid_token(value)
            response = ValidResponseSchemas(
                valid=is_valid,
                message=f"{key} is {'valid' if is_valid else 'invalid or expired'}"
            )
            valid_dict[key] = response
        else:
            valid_dict[key] = ValidResponseSchemas(valid=False, message=f"{key} is missing")

    return valid_dict


async def valid_refresh(token: TokenSchemas) -> TokenSchemas:
    if not token.refresh_token:
        raise NotRefreshToken()

    if not JWTToken.is_valid_token(token.refresh_token):
        raise InvalidToken()

    payload = JWTToken.get_payload(token.refresh_token)

    if not payload:
        raise InvalidToken()

    access_token = JWTToken.create_access_token(int(payload['sub']))

    return TokenSchemas(access_token=access_token, refresh_token=None)