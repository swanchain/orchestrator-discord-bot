# model.py
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Float, insert

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


def set_user_claim_info(discord_id: str, discord_name: str, from_wallet_address: str,
                        to_wallet_address: str, claimed_amount: float, tx_hash: str):
    query = insert(users).values(
        discord_id=discord_id,
        discord_name=discord_name,
        from_wallet_address=from_wallet_address,
        to_wallet_address=to_wallet_address,
        last_claim_time=datetime.utcnow(),
        claimed_amount=claimed_amount,
        transaction_hash=tx_hash
    )
    return query
