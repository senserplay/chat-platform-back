from distutils.command.install import value

from src.infrastructure.redis.storage.redis_storage import RedisStorage


class StatisticStorage(RedisStorage):
    def __init__(self):
        super().__init__(prefix = "statistic")

    def set_day_messages(self, value:int, key:str ="day_messages"):
        self.set_value(key, value)

    def get_day_messages(self, key:str ="day_messages"):
        self.get_value(key)

    def set_day_active_chats(self, value:int, key:str = "day_active_chats"):
        self.set_value(key, value)

    def get_day_active_chats(self, key:str = "day_active_chats"):
        self.get_value(key)
