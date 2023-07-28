from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Integer, String

Base = declarative_base()


class Config(Base):
    __tablename__ = "config"
    __schema__ = "discord_bot"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String)
    value = Column(String)
    is_active = Column(Boolean)


# get config by key
async def get_config(session: AsyncSession, key: str):
    result = await session.execute(select(Config).where(Config.key == key))
    return result.scalars().first()


# get all config that is active
async def get_all_active_config(session: AsyncSession):
    result = await session.execute(select(Config).where(Config.is_active == True))
    return result.scalars().all()
