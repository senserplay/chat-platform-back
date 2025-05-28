from datetime import datetime, timezone, time, timedelta
from zoneinfo import ZoneInfo

from loguru import logger

from src.infrastructure.postgres.repositories.message import messages_repository
from src.infrastructure.redis.storage.statistic_storage import statistics_storage

from src.infrastructure.postgres.client import SessionLocal


def get_time_range_for_msk_date(target_date: datetime):
    moscow_tz = ZoneInfo("Europe/Moscow")

    if target_date.tzinfo is None:
        target_date = target_date.replace(tzinfo=moscow_tz)

    start_of_day = datetime.combine(target_date.date(), time.min, tzinfo=moscow_tz)
    end_of_day = datetime.combine(target_date.date(), time.max, tzinfo=moscow_tz)

    start_utc = start_of_day.astimezone(timezone.utc)
    end_utc = end_of_day.astimezone(timezone.utc)

    return start_utc, end_utc

def message_data() -> None:
    logger.info("Запустил задачу")
    # Получаем вчерашнюю дату по Московскому времени
    moscow_time_yesterday = datetime.now(ZoneInfo("Europe/Moscow")) - timedelta(days=1)
    timestamp = moscow_time_yesterday.timestamp()
    chats_count = []
    with SessionLocal() as db_session:
        daily_messages = messages_repository.get_daily_message(db_session, *get_time_range_for_msk_date(moscow_time_yesterday))
    message_count = len(daily_messages)
    for message in daily_messages:
        chats_count.append(message.chat_uuid)
    chats_count = len(list(set(chats_count)))
    message_par_day = message_count
    chats_par_day = chats_count
    statistics_storage.set_daily_messages(timestamp=timestamp, value=message_par_day)
    statistics_storage.set_day_active_chats(timestamp=timestamp, value=chats_par_day)
