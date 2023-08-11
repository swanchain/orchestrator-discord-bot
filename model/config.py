from sqlalchemy import Table, Column, Integer, String, MetaData, select, event, DDL
from db.session_manager import AsyncSessionManager
from log.logger import error_logger

metadata = MetaData(schema='discord_bot')
event.listen(
    metadata, 'before_create', DDL('CREATE SCHEMA IF NOT EXISTS discord_bot')
)

config = Table('config', metadata,
               Column('id', Integer, primary_key=True),
               Column('key', String),
               Column('value', String),
               Column('is_active', Integer, default=True),
               )


async def get_config(key: str):
    async_session_manager = AsyncSessionManager()
    session = async_session_manager.get_session()
    try:
        query = select(config).where(config.c.key == key)
        result = await session.execute(query)
        row = result.fetchone()
        return row[2] if row else None
    except Exception as e:
        error_logger.error(f"Error in get_config: {e}")
        return None
    finally:
        await session.close()


async def get_all_active_config():
    async_session_manager = AsyncSessionManager()
    session = async_session_manager.get_session()
    try:
        query = select(config).where(config.c.is_active is True)
        result = await session.execute(query)
        return result
    except Exception as e:
        error_logger.error(f"Error in get_all_active_config: {e}")
        return None
    finally:
        await session.close()
