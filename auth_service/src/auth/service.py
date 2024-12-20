from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.schemas import UserSchemas


async def create_user(user_data: UserSchemas, db: AsyncSession) -> UserSchemas | None:
    try:
        user = User(
            username=user_data.username,
            email=user_data.email,
        )

        if not user_data.password:
            return None

        user.password = user_data.password

        db.add(user)
        await db.commit()


        user_data = UserSchemas.model_validate(user, from_attributes=True)
        user_data.password = None

        return user_data
    except:
        await db.rollback()
        return None


async def get_user_by_email(email: str, db: AsyncSession) -> UserSchemas | None:
    try:
        query = select(User).where(User.email == email)
        result = await db.execute(query)

        user = result.scalars().first()

        if user is None:
            return None

        return UserSchemas.model_validate(user, from_attributes=True)
    except:
        await db.rollback()
        return None


async def update_user(user_id: int, user: UserSchemas, db: AsyncSession) -> UserSchemas | None:
    try:
        update_data = {key: value for key, value in user.dict(exclude_none=True).items()}
        query = update(User).where(User.id == user_id).values(**update_data)

        await db.execute(query)
        await db.commit()

        user_query = select(User).where(User.id == user_id)

        user_instance = await db.execute(user_query)
        user_instance = user_instance.scalars().first()

        user_data = {key: value for key, value in user_instance.__dict__.items() if key != "password"}
        return UserSchemas(**user_data)
    except Exception as e:
        await db.rollback()
        return None
