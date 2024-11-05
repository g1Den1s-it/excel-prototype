from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.schemas import UserSchemas

from src.auth import service
from src.auth.exceptions import CreateUserException
from src.database import get_db_session


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
# logout