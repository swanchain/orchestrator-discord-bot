# model/config.py

from sqlalchemy import Table, Column, String, MetaData, insert, Boolean

metadata = MetaData(schema='discord_bot')

config = Table('config', metadata,
               Column('key', String, primary_key=True),
               Column('value', String),
               Column('is_active', Boolean)
               )


# insert config
def set_config(key: str, value: str, is_active: bool):
    query = insert(config).values(
        key=key,
        value=value,
        is_active=is_active
    )
    return query


# get config by key
def get_config(key: str):
    query = config.select().where(config.c.key == key)
    return query


# get all config that is active
def get_all_active_config():
    query = config.select().where(config.c.is_active is True)
    return query


# update config
def update_config(key: str, value: str, is_active: bool):
    query = config.update().where(config.c.key == key).values(
        value=value,
        is_active=str(is_active)
    )
    return query
