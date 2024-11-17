import asyncio
import os
from typing import AsyncGenerator

import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from src.database import AsyncDatabaseSessionManager, get_db_session, Base
from src.main import app

from src.auth.models import User # noqa

load_dotenv()

SQL_TEST_DATABASE_URL = (f"postgresql+asyncpg://"
                    f"{os.getenv('DB_USER')}:"
                    f"{os.getenv('DB_PASSWORD')}@"
                    f"{os.getenv('DB_HOST')}:"
                    f"{os.getenv('DB_PORT')}/"
                    f"{os.getenv('TEST_DB_NAME')}")


# init test db

session_manager = AsyncDatabaseSessionManager(SQL_TEST_DATABASE_URL)

async def test_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.session() as session:
        yield session

app.dependency_overrides[get_db_session] = test_async_session


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_db_table(event_loop):
    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_connection() -> AsyncGenerator[AsyncEngine, None]:
    async with session_manager.connect() as conn:
        yield conn

