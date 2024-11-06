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
    NotCreatedTokensError)
from src.auth.service import (get_user_by_email)
from src.auth.utils import PasswordHax, JWTToken


# create
async def valid_create_user(user_data: UserSchemas,
                      db:AsyncSession = Depends(get_db_session)) -> UserSchemas:
    user = await service.create_user(user_data, db)
    if not user:
        raise CreateUserException()
    return user
# Read
# Update
# Delete
# Login
async def valid_login(user_data: UserSchemas,
                      db: AsyncSession = Depends(get_db_session)) -> TokenSchemas:
    if not user_data.email  and not user_data.password:
        raise FieldRequiredException("'Email' and 'Password' are required!")

    user: UserSchemas | None = await get_user_by_email(user_data, db)

    if not user:
        raise InvalidEmailException()

    if not PasswordHax.verify_password(user_data, user.password):
        return InvalidPasswordException()

    tokens = TokenSchemas()
    tokens.access_token = JWTToken.create_access_token(user.id)
    tokens.refresh_token = JWTToken.create_refresh_token(user.id, user.email)

    if not tokens.access_token and not tokens.refresh_token:
        raise NotCreatedTokensError()

    return tokens

