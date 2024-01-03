from sqlalchemy.orm import DeclarativeBase
from config import Configuration
from dotenv import dotenv_values

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

config = dotenv_values(".env")


if config["TESTING_MODE"].lower() == "true":
    TESTING_MODE = True
elif config["TESTING_MODE"].lower() == "false":
    TESTING_MODE = False
else:
    raise TypeError("TESTING_MODE must be 'True' or 'False'")


if TESTING_MODE == True:
    configuration = Configuration(
        config["DB_TEST_USER"],
        config["DB_TEST_PASS"],
        config["DB_TEST_HOST"],
        config["DB_TEST_PORT"],
        config["DB_TEST_NAME"],
        config["SECRET"]
    )
else:
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


async def get_db():
    async with engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
