from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, select, event, DDL

metadata = MetaData(schema='discord_bot')
event.listen(
    metadata, 'before_create', DDL('CREATE SCHEMA IF NOT EXISTS discord_bot')
)

config = Table('config', metadata,
               Column('id', Integer, primary_key=True),
               Column('key', String),
               Column('value', String),
               Column('is_active', Boolean),
               )


def get_config(key: str):
    query = select(config).where(config.c.key == key)
    return query


def get_all_active_config():
    query = select(config).where(config.c.is_active == True)
    return query
