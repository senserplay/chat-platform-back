from fastapi import FastAPI
from .routes.core.user.api import ROUTER as USER_ROUTER


def setup(app: FastAPI):
    app.include_router(USER_ROUTER, tags=["User"])
