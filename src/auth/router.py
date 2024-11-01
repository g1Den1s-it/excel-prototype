from fastapi.routing import APIRouter

auth = APIRouter(prefix="/auth")


@auth.get("/hi/")
async def hello():
    return {"message": "Hi"}
