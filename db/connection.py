# db.py
from sqlalchemy import create_engine
from model.user import metadata
from config import get_env
from log.logger import error_logger

DATABASE_URL = get_env('DATABASE_URL')

engine = create_engine(DATABASE_URL)

try:
    engine.connect()
except Exception as e:
    error_logger.error(e, "Database connection failed")
    exit(1)


metadata.create_all(engine)  # 在数据库中创建表
