from fastapi import FastAPI
from src.presentation.fastapi.setup_routes import setup

from fastapi.middleware.cors import CORSMiddleware

from loguru import logger

import sys
import logging


logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "format": (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level> "
                "<green>(session_id={extra[session_id]})</green>"
            ),
        }
    ],
    extra={"session_id": "No session"},
)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


def setup_uvicorn_loggers():
    intercept_handler = InterceptHandler()
    loggers = [
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn")
    ]

    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []
        uvicorn_logger.propagate = False
        uvicorn_logger.addHandler(intercept_handler)


setup_uvicorn_loggers()

app = FastAPI(
    title="ChatPlatform",
    description="Менеджер платформы чатов",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup(app)
