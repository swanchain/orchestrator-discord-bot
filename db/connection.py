# db.py
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from config import get_env
from log.logger import error_logger, info_logger

DATABASE_URL = get_env('ASYNC_DATABASE_URL')


async def connect_database() -> AsyncEngine:
    """
    Connect to the database asynchronously and return the engine.
    :return: AsyncEngine
    """
    info_logger.info(f'-- Connecting to database at {DATABASE_URL} at {datetime.utcnow()}')
    try:
        engine = create_async_engine(DATABASE_URL)
    except Exception as e:
        error_logger.error(f"Database connection failed: {e}")
        exit(1)
    return engine
