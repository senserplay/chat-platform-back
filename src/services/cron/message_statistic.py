from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlmodel import Session as DBSession

from src.infrastructure.postgres.repositories.message import messages_repository
from src.infrastructure.redis.storage.statistic_storage import statistics_storage

from fastapi import Depends

from src.infrastructure.postgres.client import get_db_session


def message_data(db_session: DBSession = Depends(get_db_session))->None:
    moscow_date = datetime.now(ZoneInfo("Europe/Moscow"))- timedelta(days=1)
    chats_count = []
    daily_messages = messages_repository.get_daily_message(db_session, moscow_date)
    message_count = len(daily_messages)
    for message in daily_messages:
        chats_count.append(message.chat_uuid)
    chats_count = set(chats_count)
    message_par_day = {moscow_date:message_count}
    chats_par_day = {moscow_date:chats_count}
    statistics_storage.set_daily_messages(value= message_par_day)
    statistics_storage.set_day_active_chats(value= chats_par_day)


