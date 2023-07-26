# db.py
from datetime import datetime

from sqlalchemy import inspect, create_engine

from model.user import metadata
from config import get_env
from log.logger import error_logger, info_logger

DATABASE_URL = get_env('SYNC_DATABASE_URL')


def create_table():
    engine = create_engine(DATABASE_URL)
    try:
        info_logger.info(f'-- Connecting to database at {datetime.utcnow()} to check if table "users" exists')
        inspector = inspect(engine)
        if not inspector.has_table("users"):
            info_logger.info(f'-- Table "users" does not exist. Creating table "users" at {datetime.utcnow()}')
            metadata.create_all(engine)
        else:
            info_logger.info(f'-- Table "users" exists. Skipping table creation at {datetime.utcnow()}')
    except Exception as e:
        error_logger.error(f"Database init failed: {e}")
        exit(1)
    finally:
        engine.dispose()
