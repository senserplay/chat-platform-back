from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.core.logger.default import setup_uvicorn_loggers
from src.presentation.fastapi.setup_routes import setup

from fastapi.middleware.cors import CORSMiddleware

from apscheduler.schedulers.background import BackgroundScheduler
from src.services.cron.message_statistic import message_data

scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_uvicorn_loggers()
    logger.info("🔌 Сервер запущен")
    scheduler.add_job(
        message_data, 'cron', hour=0, minute=0
    )
    scheduler.start()
    yield
    scheduler.shutdown()
    logger.info("🔌 Сервер останавливается.")


app = FastAPI(
    title="ChatPlatform",
    description="Менеджер платформы чатов",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://chat-platform.amurushkin.ru"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup(app)
