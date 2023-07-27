# db.py
from datetime import datetime

from sqlalchemy import inspect, create_engine

from model.user import metadata
from model.config import metadata as config_metadata
from services.config_services import get_env_from_file, set_all_config
from log.logger import error_logger, info_logger

DATABASE_URL = "postgresql://" + get_env_from_file('DATABASE_URL')


def create_table():
    engine = create_engine(DATABASE_URL)
    try:
        info_logger.info(f'-- Connecting to database at {datetime.utcnow()} to check if table "users" exists')
        inspector = inspect(engine)
        # Check if table users exists
        if not inspector.has_table("users"):
            info_logger.info(f'-- Table "users" does not exist. Creating table "users" at {datetime.utcnow()}')
            metadata.create_all(engine)
        else:
            info_logger.info(f'-- Table "users" exists. Skipping table creation at {datetime.utcnow()}')

        # Check if table config exists
        if not inspector.has_table("config"):
            print(inspector.has_table("config"))
            info_logger.info(f'-- Table "config" does not exist. Creating table "config" at {datetime.utcnow()}')
            config_metadata.create_all(engine)

        else:
            info_logger.info(f'-- Table "config" exists. Skipping table creation at {datetime.utcnow()}')
        set_all_config()


    except Exception as e:
        error_logger.error(f"Database init failed: {e}")
        exit(1)
    finally:
        engine.dispose()
