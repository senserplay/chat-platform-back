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
            redis_client.set(self.format_key(key), value, ex=expiration)
        else:
            redis_client.set(self.format_key(key), value)

    def get_value(self, key):
        """
        Получение значения по ключу.
        :param key: Ключ
        :return: Значение или None, если ключ не существует
        """
        return redis_client.get(self.format_key(key))

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
