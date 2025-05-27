from typing import List, Dict

from fastapi import APIRouter

from src.infrastructure.redis.storage.statistic_storage import statistics_storage

ROUTER = APIRouter(prefix="/statistic")

@ROUTER.get(
    "/daily_messages",
    response_model=Dict,
    summary="Получить количество сообщений за неделю",
)
async def get_all_daily_messages()->Dict:
    return statistics_storage.get_all_daily_messages()

@ROUTER.get(
    "/day_active_chats",
    response_model=Dict,
    summary="Получить количество активных чатов за неделю",
)
async def get_all_day_active_chats()->Dict:
    return statistics_storage.get_all_day_active_chats()