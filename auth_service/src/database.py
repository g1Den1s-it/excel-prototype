import os
from collections.abc import AsyncIterator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

SQL_DATABASE_URL = (f"postgresql+asyncpg://"
                    f"{os.getenv('DB_USER')}:"
                    f"{os.getenv('DB_PASSWORD')}@"
                    f"{os.getenv('DB_HOST')}:"
                    f"{os.getenv('DB_PORT')}/"
                    f"{os.getenv('DB_NAME')}")

class AsyncDatabaseSessionManager:
    def __init__(self):
        self._engine= None
        self._session = None

    async def init(self) -> None:
        self._engine = create_async_engine(SQL_DATABASE_URL, future=True, echo=True)
        self._session = async_sessionmaker(
            self._engine, expire_on_commit=False, class_= AsyncSession
        )

    async def session(self) -> AsyncIterator[AsyncSession]:
        if not self._session or not self._engine:
            raise Exception("AsyncDataSessionManager is not initialized!")

        session: AsyncSession = self._session()

        try:
            yield session
        except Exception:
            await session.rollback()
            await session.close()
            raise
        finally:
            await session.close()


async_session_manager = AsyncDatabaseSessionManager()
async_session_manager.init()

Base = declarative_base()

async def get_db_session():
    async with async_session_manager.session() as session:
        yield session
