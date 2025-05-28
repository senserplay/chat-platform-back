import json
from typing import Union

from pydantic import BaseModel

from src.infrastructure.redis.client import redis_client


class RedisStorage:
    def __init__(self, prefix="chat-platform"):
        """
        Инициализация базового хранилища Redis.
        :param prefix: Общий префикс для всех ключей (по умолчанию "chat-platform").
        """
        self.prefix = prefix

    def set_value(self, key, value, expiration=None):
        """
        Запись значения в Redis.
        :param key: Ключ
        :param value: Значение
        :param expiration: Время жизни ключа в секундах (опционально)
        """
        if expiration:
            redis_client.set(self.format_key(key), self.format_value(value), ex=expiration)
        else:
            redis_client.set(self.format_key(key), self.format_value(value))

    def get_value(self, key):
        """
        Получение значения по ключу.
        :param key: Ключ
        :return: Значение или None, если ключ не существует
        """
        return self.extract_value(redis_client.get(self.format_key(key)))

    def delete_key(self, key):
        """
        Удаление ключа.
        :param key: Ключ
        :return: True, если ключ был удален, иначе False
        """
        return redis_client.delete(self.format_key(key)) > 0

    def exists(self, key):
        """
        Проверка существования ключа.
        :param key: Ключ
        :return: True, если ключ существует, иначе False
        """
        return redis_client.exists(self.format_key(key)) > 0

    def format_key(self, key):
        """
        Форматирование ключа с добавлением префикса.
        :param key: Исходный ключ
        :return: Полный ключ с префиксом
        """
        return f"{self.prefix}:{key}"

    def hash_set(self, key: str, data: dict, ttl: Union[int, None] = None):
        """
        Сохраняет данные в хеш-таблицу в Redis.

        :param key: Основной ключ хеша (например, session_id:user_id).
        :param data: Словарь с данными, которые будут сохранены в хеше.
        :param ttl: Время жизни ключа (в секундах).
        """
        redis_key = self.format_key(key)
        # Устанавливаем каждое поле хеша
        for field, value in data.items():
            redis_client.hset(redis_key, field, json.dumps(value))

        if ttl:
            redis_client.expire(redis_key, ttl)

    def hash_exists(self, key: str, field: str = None):
        """
        Проверяет, существует ли ключ хеша или поле внутри хеша в Redis.

        :param key: Основной ключ хеша.
        :param field: Поле внутри хеша. Если указано, проверяется существование поля.
        :return: True, если ключ или поле существует, иначе False.
        """
        redis_key = self.format_key(key)
        if field:
            return redis_client.hexists(redis_key, field)
        return redis_client.exists(redis_key) > 0

    def hash_get(self, key: str, field: str = None):
        """
        Получает одно или все поля хеша в Redis.

        :param key: Основной ключ хеша.
        :param field: Если указано, возвращает только это поле.
        :return: Значение поля или словарь с полями и значениями.
        """
        redis_key = self.format_key(key)
        if field:
            raw_value = redis_client.hget(redis_key, field)
            return json.loads(raw_value) if raw_value else None
        else:
            raw_values = redis_client.hgetall(redis_key)
            return {k.decode(): json.loads(v) for k, v in raw_values.items()}

    def hash_delete(self, key: str, field: str = None):
        """
        Удаляет указанное поле из хеша. Если хеш становится пустым, удаляет сам ключ.
        :param key: Ключ хеша.
        :param field: Поле для удаления.
        """
        redis_key = self.format_key(key)
        # Удаляем указанное поле
        redis_client.hdel(redis_key, field)

        # Проверяем, пуст ли хеш
        if redis_client.hlen(redis_key) == 0:
            # Если хеш пуст, удаляем сам ключ
            redis_client.delete(redis_key)

    def list_get(self, key: str, start=0, end=-1):
        return [
            self.extract_value(i)
            for i in redis_client.lrange(self.format_key(key), start, end)
        ]

    def list_push(
            self, key: str, value: Union[dict, float, BaseModel, str], ttl=3600
    ):
        """
        Добавляет значение в начало списка в Redis.
        :param key: Ключ списка.
        :param value: Значение для добавления.
        :param ttl: Время жизни ключа (в секундах).
        """
        formatted_value = (
            value if isinstance(value, str) else self.format_value(value)
        )
        redis_client.lpush(self.format_key(key), formatted_value)
        redis_client.expire(self.format_key(key), ttl)

    def extract_value(self, value):
        if value is None:
            return None
        return json.loads(value)

    def format_value(self, value: Union[dict, BaseModel, float]):
        return json.dumps(value) if isinstance(value, dict) else str(value)

    def keys(self, wildcard: str):
        raw_keys = redis_client.keys(self.format_key(wildcard))
        return [key.decode().replace(self.prefix, "") for key in raw_keys]