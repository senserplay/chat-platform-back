from fastapi import FastAPI
from .routes.core.user.api import ROUTER as USER_ROUTER
from .routes.core.message.api import ROUTER as MESSAGE_ROUTER
from .routes.core.chat.api import ROUTER as CHAT_ROUTER
from .routes.core.invite.api import ROUTER as INVITE_ROUTER
from .routes.core.statistics.api import ROUTER as STATISTICS_ROUTER
from .websockets.message.ws import ROUTER as MESSAGE_WS


def setup(app: FastAPI):
    app.include_router(USER_ROUTER, tags=["User"])
    app.include_router(MESSAGE_ROUTER, tags=["Message"])
    app.include_router(CHAT_ROUTER, tags=["Chat"])
    app.include_router(INVITE_ROUTER, tags=["Invite"])
    app.include_router(MESSAGE_WS, tags=["Message"])
    app.include_router(STATISTICS_ROUTER, tags=["Statistics"])
