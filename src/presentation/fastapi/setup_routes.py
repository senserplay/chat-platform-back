from fastapi import FastAPI
from .routes.core.user.api import ROUTER as USER_ROUTER
from .routes.core.message.api import ROUTER as MESSAGE_ROUTER
from .routes.core.chat.api import ROUTER as CHAT_ROUTER


def setup(app: FastAPI):
    app.include_router(USER_ROUTER, tags=["User"])
    app.include_router(MESSAGE_ROUTER, tags=["Message"])
    app.include_router(CHAT_ROUTER, tags=["Chat"])
