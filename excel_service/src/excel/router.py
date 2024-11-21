from fastapi import APIRouter


excel = APIRouter(prefix="/excel")

@excel.get("")
async def hello():
    return {"message": "HI!"}