from fastapi import FastAPI

from src.excel.router import excel
app = FastAPI()

app.include_router(excel)

