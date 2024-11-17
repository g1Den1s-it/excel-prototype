from alembic.util import status
from fastapi.params import Depends
from fastapi.routing import APIRouter
from fastapi import status

from src.auth.schemas import UserSchemas, ValidResponseSchemas

from src.auth.dependencies import (
    valid_create_user,
    valid_login,
    valid_new_data,
    valid_token
)

from src.auth.schemas import TokenSchemas


auth = APIRouter(prefix="/auth")


# create
@auth.post("/create-user/",
            response_model=UserSchemas,
            status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSchemas = Depends(valid_create_user)):
    return user

# Login
@auth.post("/login/",
          response_model=TokenSchemas,
          status_code=status.HTTP_200_OK)
def login(user: UserSchemas = Depends(valid_login)):
    return user

# Update
@auth.put("/update/",
           response_model=UserSchemas,
           status_code=status.HTTP_200_OK)
def update_user(user: UserSchemas = Depends(valid_new_data)):
    return user


@auth.post("/check-token/",
           response_model=dict[str, ValidResponseSchemas],
           status_code=200)
async def check_token(valid: ValidResponseSchemas = Depends(valid_token)):
    return valid