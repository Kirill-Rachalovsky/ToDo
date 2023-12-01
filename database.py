from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Configuration
from dotenv import dotenv_values

config = dotenv_values(".env")

configuration = Configuration(
    config["DB_USER"],
    config["DB_PASS"],
    config["DB_HOST"],
    config["DB_PORT"],
    config["DB_NAME"],
    config["SECRET"]
)

DATABASE_URL = (f"postgresql://{configuration.db_user}:{configuration.db_pass}@{configuration.db_host}:"
                f"{configuration.db_port}/{configuration.db_name}")

# DATABASE_URL = "postgresql://postgres:admin1234@localhost:5432/ToDo"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

