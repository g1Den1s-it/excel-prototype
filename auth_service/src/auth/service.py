from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.schemas import UserSchemas
from src.auth.utils import PasswordHax


async def create_user(user_data: UserSchemas, db: AsyncSession) -> UserSchemas | None:
    try:
        user = User(
            username=user_data.username,
            email=user_data.email,
        )

        user.password = PasswordHax.create_password_hash(user_data.password)

        db.add(user)
        await db.commit()

        return user.dict(exclude={"password"})
    except:
        await db.rollback()
        return None