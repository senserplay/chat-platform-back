from typing import List, Dict

from fastapi import APIRouter

from src.infrastructure.redis.storage.statistic_storage import statistics_storage

ROUTER = APIRouter(prefix="/statistic")


@ROUTER.get(
    "/daily_messages",
    response_model=Dict,
    summary="Получить количество сообщений за неделю",
)
async def get_all_daily_messages() -> Dict:
    return statistics_storage.get_all_daily_messages()


@ROUTER.get(
    "/day_active_chats",
    response_model=Dict,
    summary="Получить количество активных чатов за неделю",
)
async def get_all_day_active_chats() -> Dict:
    return statistics_storage.get_all_day_active_chats()


@ROUTER.post(
    "/statistics"
)
async def set_statistics():
    # Получаем вчерашнюю дату по Московскому времени
    from datetime import datetime
    from zoneinfo import ZoneInfo
    from datetime import timedelta
    from src.infrastructure.postgres.client import SessionLocal
    from src.infrastructure.postgres.repositories.message import messages_repository
    from src.services.cron.message_statistic import get_time_range_for_msk_date
    for day in range(1, 8):
        moscow_time_yesterday = datetime.now(ZoneInfo("Europe/Moscow")) - timedelta(days=day)
        timestamp = moscow_time_yesterday.timestamp()
        chats_count = []
        with SessionLocal() as db_session:
            daily_messages = messages_repository.get_daily_message(db_session,
                                                                   *get_time_range_for_msk_date(moscow_time_yesterday))
        message_count = len(daily_messages)
        for message in daily_messages:
            chats_count.append(message.chat_uuid)
        chats_count = len(list(set(chats_count)))
        message_par_day = message_count
        chats_par_day = chats_count
        statistics_storage.set_daily_messages(timestamp=timestamp, value=message_par_day, days=8 - day)
        statistics_storage.set_day_active_chats(timestamp=timestamp, value=chats_par_day, days=8 - day)
    return {"status": "ok"}
