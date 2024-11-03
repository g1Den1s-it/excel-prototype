from fastapi.params import Depends
from fastapi.routing import APIRouter

from auth_service.src.auth.schemas import UserSchemas

auth = APIRouter(prefix="/auth")


# create
@auth.post("/create-user/",
            response_model=UserSchemas,
            status_code=201)
async def create_user(user: UserSchemas = Depends()):
    pass
# Read
# Update
# Delete
# Login
# logout