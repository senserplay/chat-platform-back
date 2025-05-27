from datetime import datetime
from typing import List, Dict
from src.application.schemas.message import MessageSchema
from src.infrastructure.redis.storage.redis_storage import RedisStorage


class StatisticStorage(RedisStorage):
    def __init__(self):
        super().__init__(prefix="statistic")

    def set_daily_messages(self, timestamp: int, value: int, key: str = "daily_messages"):

        self.set_value(f"{key}:{timestamp}",value, expiration=60 * 60 * 24 * 7)

    def get_all_daily_messages(self, key: str = "daily_messages"):
        ans = {}
        keys = self.keys(f"{key}:*")
        for k in sorted(keys):
            timestamp = k[k.rfind(":")+1:]
            dt = datetime.fromtimestamp(float(timestamp))

            # Форматируем вывод по своему желанию
            formatted_date = dt.strftime("%Y-%m-%d")
            ans[formatted_date]=self.get_value(key = k[1:])
        return ans

    def set_day_active_chats(self, timestamp: int, value: int, key: str = "day_active_chats"):
        self.set_value(f"{key}:{timestamp}",value, expiration=60 * 60 * 24 * 7)

    def get_all_day_active_chats(self, key: str = "day_active_chats"):
        ans = {}
        keys = self.keys(f"{key}:*")
        for k in sorted(keys):
            timestamp = k[k.rfind(":") + 1:]
            dt = datetime.fromtimestamp(float(timestamp))

            # Форматируем вывод по своему желанию
            formatted_date = dt.strftime("%Y-%m-%d")
            ans[formatted_date] = self.get_value(key=k[1:])
        return ans


statistics_storage = StatisticStorage()
