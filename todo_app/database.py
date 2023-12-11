from sqlalchemy.orm import DeclarativeBase
from config import Configuration
from dotenv import dotenv_values

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

config = dotenv_values(".env")

configuration = Configuration(
    config["DB_USER"],
    config["DB_PASS"],
    config["DB_HOST"],
    config["DB_PORT"],
    config["DB_NAME"],
    config["SECRET"]
)

DATABASE_URL = (f"postgresql+asyncpg://{configuration.db_user}:{configuration.db_pass}@{configuration.db_host}:"
                f"{configuration.db_port}/{configuration.db_name}")

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

