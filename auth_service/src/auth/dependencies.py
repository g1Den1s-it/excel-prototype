from fastapi import Header
from fastapi.params import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import service
from src.database import get_db_session
from src.auth.schemas import (
    UserSchemas, TokenSchemas)
from src.auth.exceptions import (
    CreateUserException,
    FieldRequiredException,
    InvalidEmailException,
    InvalidPasswordException,
    NotCreatedTokensError,
    NotAuthorizationException,
    InvalidToken,
    NotUpdateUserError)
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
                      db:AsyncSession = Depends(get_db_session)) -> UserSchemas:
    user = await service.create_user(user_data, db)
    if not user:
        raise CreateUserException()
    return user


async def valid_login(user_data: UserSchemas,
                      db: AsyncSession = Depends(get_db_session)) -> TokenSchemas:
    if not user_data.email  and not user_data.password:
        raise FieldRequiredException("'Email' and 'Password' are required!")

    user: UserSchemas | None = await get_user_by_email(user_data.email, db)

    if not user:
        raise InvalidEmailException()

    if not PasswordHax.verify_password(user_data.password, user.password):
        return InvalidPasswordException()

    tokens = TokenSchemas()
    tokens.access_token = JWTToken.create_access_token(user.id)
    tokens.refresh_token = JWTToken.create_refresh_token(user.id, user.email)

    if not tokens.access_token and not tokens.refresh_token:
        raise NotCreatedTokensError()

    return tokens


async def valid_new_data(new_user_data: UserSchemas,
                   authorization: str = Header(None),
                   db: AsyncSession = Depends(get_db_session)) -> UserSchemas:

    check_authorization(authorization)

    user_payload = JWTToken.get_payload(authorization.split(" ")[1])

    if not user_payload:
        raise InvalidToken()

    user: UserSchemas = await service.update_user(int(user_payload["sub"]),new_user_data, db)

    if not user:
        raise NotUpdateUserError()

    return user
