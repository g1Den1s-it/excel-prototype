from fastapi import FastAPI

from src.auth.router import auth

app = FastAPI()
app.include_router(auth)

