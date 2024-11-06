from alembic.util import status
from fastapi.params import Depends
from fastapi.routing import APIRouter
from fastapi import status

from src.auth.schemas import UserSchemas

from src.auth.dependencies import valid_create_user, valid_login

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
# Delete
# logout