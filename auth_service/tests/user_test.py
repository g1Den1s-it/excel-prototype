import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.util import await_only


class TestUser:
    test_user_data = {
        "username": "test-username",
        "email": "test@test.com",
        "password": "q1w2e3r4t5y6"
    }
    login_response = None

    @pytest.mark.asyncio
    async def test_create_user(self, ac: AsyncClient, async_connection: AsyncEngine):

        res = await ac.post("/auth/create-user/", json=self.test_user_data)

        assert res.status_code == 201
        assert res.json().get("username") == self.test_user_data['username']
        assert res.json().get("email") == self.test_user_data['email']


    @pytest.mark.asyncio
    async def test_login_user(self, ac: AsyncClient, async_connection: AsyncEngine):
        res = await ac.post("/auth/login/", json=self.test_user_data)

        assert res.status_code == 200
        assert res.json().get("refresh_token")
        assert res.json().get("access_token")
        TestUser.login_response = res.json()


    @pytest.mark.asyncio
    async def test_update_user(self, ac: AsyncClient, async_connection: AsyncEngine):
        if not TestUser.login_response:
            assert False, "Login response is not available or None"

        res =  await ac.put("/auth/update/",
                            headers={"Authorization": f"Bearer {TestUser.login_response.get("access_token")}"},
                            json={"username": "new-test-username"})

        assert res.status_code == 200
        assert res.json().get("username") == "new-test-username"


    @pytest.mark.asyncio
    async def test_update_user_invalid_token(self, ac: AsyncClient, async_connection: AsyncEngine):
        if not TestUser.login_response:
            assert False, "Login response is not available or None"

        res =  await ac.put("/auth/update/",
                            headers={"Authorization": f"{TestUser.login_response.get("access_token")}"},
                            json={"username": "new-test-username"})

        assert res.status_code == 401


    @pytest.mark.asyncio
    async def test_check_token(self, ac: AsyncClient):
        if not TestUser.login_response:
            assert False, "Login response is not available or None"

        res = await ac.post("/auth/check-token/",
                            json={"access_token": TestUser.login_response.get("access_token")})

        assert res.status_code == 200
        assert res.json().get("access_token")['valid'] == True
        assert res.json().get("refresh_token")['valid'] == False


    @pytest.mark.asyncio
    async def test_check_invalid_token(self, ac: AsyncClient):
        if not TestUser.login_response:
            assert False, "Login response is not available or None"

        res = await ac.post("/auth/check-token/",
                            json={"access_token": TestUser.login_response.get("access_token")+"w12e1er12"})

        assert res.status_code == 200
        assert res.json().get("access_token")['valid'] == False


    @pytest.mark.asyncio
    async def test_refresh_token(self, ac: AsyncClient):
        if not TestUser.login_response:
            assert False, "Login response is not available or None"

        res = await ac.post("/auth/refresh-token/",
                                json={"refresh_token": TestUser.login_response.get("refresh_token")})

        assert res.status_code == 200
        assert res.json().get("access_token")


    @pytest.mark.asyncio
    async def test_refresh_invalid_token(self, ac: AsyncClient):
        if not TestUser.login_response:
            assert False, "Login response is not available or None"

        res = await ac.post("/auth/refresh-token/",
                                json={"refresh_token": TestUser.login_response.get("refresh_token")+"dqwd"})

        assert res.status_code == 401
