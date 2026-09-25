from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()