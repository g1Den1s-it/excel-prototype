from fastapi.params import Depends
from fastapi.routing import APIRouter
from fastapi import status

from src.auth.schemas import UserSchemas

from src.auth.dependencies import valid_create_user

auth = APIRouter(prefix="/auth")


# create
@auth.post("/create-user/",
            response_model=UserSchemas,
            status_code=status.HTTP_201_CREATED)
async def create_user(user: UserSchemas = Depends(valid_create_user)):
    return user
# Read
# Update
# Delete
# Login
# logout