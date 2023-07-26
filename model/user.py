# model.py

from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Float

metadata = MetaData(schema='discord_bot')

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('discord_id', String),
              Column('discord_name', String),
              Column('from_wallet_address', String),
              Column('to_wallet_address', String),
              Column('last_claim_time', DateTime),
              Column('claimed_amount', Float),
              Column('transaction_hash', String),
              )
