from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.core.logger.default import setup_uvicorn_loggers
from src.presentation.fastapi.setup_routes import setup

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_uvicorn_loggers()
    logger.info("🔌 Сервер запущен")
    yield
    logger.info("🔌 Сервер останавливается.")


app = FastAPI(
    title="ChatPlatform",
    description="Менеджер платформы чатов",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup(app)
