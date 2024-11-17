import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine


class TestUser:
    test_user_data = {
        "username": "test-username",
        "email": "test@test.com",
        "password": "q1w2e3r4t5y6"
    }


    @pytest.mark.asyncio
    async def test_create_user(self, ac: AsyncClient, async_connection: AsyncEngine):

        res = await ac.post("/auth/create-user/", json=self.test_user_data)

        assert res.status_code == 201
        assert res.json().get("username") == self.test_user_data['username']
        assert res.json().get("email") == self.test_user_data['email']


    @pytest.mark.asyncio
    async def test_login_user(self, ac: AsyncClient, async_connection: AsyncEngine):
        res = await ac.post("/auth/login/", json=self.test_user_data)

        print(res.json())
        assert res.status_code == 200