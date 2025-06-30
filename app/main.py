from fastapi import FastAPI

from app.configs.db import init_db
from app.routers.base import api_router

app = FastAPI()


def include_router(fastapi_app):
    # app.mount("/admin", admin_app)
    fastapi_app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    init_db()
    include_router(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}
