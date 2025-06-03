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
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    from src.infrastructure.postgres.client import SessionLocal
    from src.infrastructure.postgres.repositories.message import messages_repository
    from src.services.cron.message_statistic import get_time_range_for_msk_date

    moscow_tz = ZoneInfo("Europe/Moscow")
    now = datetime.now(moscow_tz)

    for ttl_days in range(1, 8):  # 1 (самый старый) до 7 (вчера)
        days_ago = 8 - ttl_days   # 7, 6, ..., 1
        msk_date = now - timedelta(days=days_ago)

        start_of_day = msk_date.replace(hour=0, minute=0, second=0, microsecond=0)
        timestamp = int(start_of_day.timestamp())

        with SessionLocal() as db_session:
            start, end = get_time_range_for_msk_date(msk_date)
            daily_messages = messages_repository.get_daily_message(db_session, start, end)

        message_count = len(daily_messages)
        chat_count = len(set(msg.chat_uuid for msg in daily_messages))

        statistics_storage.set_daily_messages(
            timestamp=timestamp,
            value=message_count,
            days=ttl_days
        )
        statistics_storage.set_day_active_chats(
            timestamp=timestamp,
            value=chat_count,
            days=ttl_days
        )

    return {"status": "ok"}