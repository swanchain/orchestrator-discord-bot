# db.py
from datetime import datetime

from sqlalchemy import inspect, create_engine

from model.user import metadata
from services.config_services import get_env_from_file
from log.logger import error_logger, info_logger

DATABASE_URL = "postgresql://" + get_env_from_file('DATABASE_URL')
engine = create_engine(DATABASE_URL)
# config_manager = ConfigManager(engine)


# def create_table():
#     try:
#         info_logger.info(f'-- Connecting to database at {datetime.utcnow()} to check if table "users" exists')
#         inspector = inspect(engine)
#         # Check if table users exists
#         if not inspector.has_table("discord_bot.users"):
#             info_logger.info(f'-- Table "users" does not exist. Creating table "users" at {datetime.utcnow()}')
#             try:
#                 metadata.create_all(engine)
#             except Exception as e:
#                 error_logger.error(f"Table 'users' created failed: {e}")
#                 exit(1)
#         else:
#             info_logger.info(f'-- Table "users" exists. Skipping table creation at {datetime.utcnow()}')
#         if not inspector.has_table('discord_bot.config'):
#             info_logger.info(f'-- Table "config" does not exist. Creating table "config" at {datetime.utcnow()}')
#             try:
#                 Base.metadata.create_all(engine)
#             except Exception as e:
#                 error_logger.error(f"Table 'config' created failed: {e}")
#                 exit(1)
#         config_manager.set_all_config()
#     except Exception as e:
#         error_logger.error(f"Database init failed: {e}")
#         exit(1)
#     finally:
#         engine.dispose()
