from fastapi import FastAPI
from .routes.core.user.api import ROUTER as USER_ROUTER
from .routes.core.message.api import ROUTER as MESSAGE_ROUTER


def setup(app: FastAPI):
    app.include_router(USER_ROUTER, tags=["User"])
    app.include_router(MESSAGE_ROUTER, tags=["Message"])
