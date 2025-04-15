from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import env_settings
from sqlmodel import Session

Base = declarative_base()

DATABASE_URL = (f"postgresql://{env_settings.PG_USERNAME}:{env_settings.PG_PASSWORD}@"
                f"{env_settings.PG_HOST}:{env_settings.PG_PORT}/{env_settings.PG_DATABASE}")

engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db_session() -> Session:
    with Session(engine) as session:
        yield session
