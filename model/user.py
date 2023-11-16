# model.py
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Float, insert, event, DDL

from log.logger import error_logger,warning_logger

metadata = MetaData(schema='discord_bot')
event.listen(
    metadata, 'before_create', DDL('CREATE SCHEMA IF NOT EXISTS discord_bot')
)


users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('discord_id', String),
              Column('discord_name', String),
              Column('from_wallet_address', String),
              Column('to_wallet_address', String),
              Column('last_claim_time', DateTime),
              Column('claimed_amount', Float),
              Column('transaction_hash', String),
              Column('token_symbol', String)
              )


def set_user_claim_info(discord_id: str, discord_name: str, from_wallet_address: str,
                        to_wallet_address: str, claimed_amount: float, tx_hash: str, token_symbol: str):
    query = insert(users).values(
        discord_id=discord_id,
        discord_name=discord_name,
        from_wallet_address=from_wallet_address,
        to_wallet_address=to_wallet_address,
        last_claim_time=datetime.utcnow(),
        claimed_amount=claimed_amount,
        transaction_hash=tx_hash,
        token_symbol=token_symbol
    )
    return query
