# db.py
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from log.logger import error_logger, info_logger
from services.config_services import get_env_from_file

DATABASE_URL = "postgresql+asyncpg://" + get_env_from_file('DATABASE_URL')


async def connect_database() -> AsyncEngine:
    """
    Connect to the database asynchronously and return the engine.
    :return: AsyncEngine
    """
    info_logger.info(f'-- Connecting to database at {DATABASE_URL} at {datetime.utcnow()}')
    try:
        engine = create_async_engine(DATABASE_URL)
        if not engine:
            error_logger.error(f"Database connection failed: {DATABASE_URL}")
            exit(1)
        else:
            info_logger.info(f'-- Connected to database at {datetime.utcnow()}')
    except Exception as e:
        error_logger.error(f"Database connection failed: {e}")
        exit(1)
    return engine
