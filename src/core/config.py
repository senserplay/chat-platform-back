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
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_DAYS: int
    RESEND_API_KEY: str
    MAILER_SENDER_FROM_ADDRESS: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


env_settings = Settings()
