# model.py
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Float



metadata = MetaData()

users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('discord_id', String),
    Column('discord_name', String),
    Column('wallet_address', String),
    Column('last_claim_time', DateTime),
    Column('claimed_amount', Float),
)
