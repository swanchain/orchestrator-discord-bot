from sqlalchemy import Table, Column, Integer, String, MetaData, select, event, DDL, and_
from db.session_manager import AsyncSessionManager
from log.logger import error_logger
from utils.get_env_config import get_env_from_file

metadata = MetaData(schema='discord_bot')
event.listen(
    metadata, 'before_create', DDL('CREATE SCHEMA IF NOT EXISTS discord_bot')
)

config = Table('config', metadata,
               Column('id', Integer, primary_key=True),
               Column('key', String),
               Column('value', String),
               Column('is_active', Integer, default=True),
               Column('note', String),
               Column('mode', String)
               )

bot_config = get_env_from_file('bot_mode')


# Add environment variables to .env file to control the bot running mode:
# TODO: Change the bot_mode to 'PROD' when deploying to production in the database
async def get_config(key: str):
    async_session_manager = AsyncSessionManager()
    session = async_session_manager.get_session()
    try:
        query = select(config).where(and_(config.c.key == key, config.c.is_active == 1, config.c.mode == bot_config))
        result = await session.execute(query)
        row = result.fetchone()
        return row[2] if row else None
    except Exception as e:
        error_logger.error(f"Error in get_config: {e}")
        return None
    finally:
        await session.close()
