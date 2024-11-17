from sqlalchemy import select
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
        user_data = {key: value for key, value in user.__dict__.items() if key != "password"}
        return UserSchemas(**user_data)
    except:
        await db.rollback()
        return None


async def get_user_by_email(email: str, db: AsyncSession):
    try:
        query = select(User).where(User.email == email)
        result = await db.execute(query)

        user = result.scalars().first()

        return UserSchemas(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            surname=user.surname
        )
    except:
        await db.rollback()
        return None
