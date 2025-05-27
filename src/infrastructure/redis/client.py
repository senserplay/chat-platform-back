import redis

from src.core.config import env_settings

redis_client = redis.Redis(
    host=env_settings.REDIS_HOST,
    port=env_settings.REDIS_PORT,
    db=env_settings.REDIS_DB_INDEX,
    username=env_settings.REDIS_USERNAME,
    password=env_settings.REDIS_PASSWORD
)
