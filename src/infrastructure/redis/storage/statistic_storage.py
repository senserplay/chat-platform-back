from typing import List, Dict

from src.application.schemas.message import MessageSchema
from src.infrastructure.redis.storage.redis_storage import RedisStorage


class StatisticStorage(RedisStorage):
    def __init__(self):
        super().__init__(prefix="statistic")

    def set_daily_messages(self, value: Dict, key: str = "daily_messages"):
        self.set_value(key, value, expiration=60 * 60 * 24 * 7)

    def get_daily_messages(self, key: str = "daily_messages"):
        self.get_value(key)

    def set_day_active_chats(self, value: Dict, key: str = "day_active_chats"):
        self.set_value(key, value, expiration=60 * 60 * 24 * 7)

    def get_day_active_chats(self, key: str = "day_active_chats"):
        self.get_value(key)


statistics_storage = StatisticStorage
