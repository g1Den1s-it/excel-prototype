from fastapi import FastAPI

from auth.src.auth.router import auth

app = FastAPI()
app.include_router(auth)

