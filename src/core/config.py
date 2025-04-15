from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PG_USERNAME: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int
    PG_DATABASE: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB_INDEX: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env_settings = Settings()
