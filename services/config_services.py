import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from log.logger import error_logger, warning_logger
from model.config import set_config, get_all_active_config


def set_all_config():
    set_config('BOT_TOKEN', 'MTEzMzU5Nzc4MTExNDc2OTQ5MA.GxTU1m.CAIZnG6SHmaHm4m3HI421TKdx6QcRkJ4XvNlX0', True)
    set_config('BOT_GUILD', '你们都是大屁眼子', True)
    set_config('FROM_WALLET_ADDRESS', '0x29eD49c8E973696D07E7927f748F6E5Eacd5516D', True)
    set_config('CLAIMED_AMOUNT', '5', True)
    set_config('PRIVATE_KEY', '895bcb462f77386e68b726666ee9a026ad87078086aa0e5c64f681a090c8265a', True)
    set_config('CONTRACT_ADDRESS', '0x3CF24790B3af64029564E81B67aF299dB83Fd9e3', True)
    set_config('RPC_ENDPOINT', 'https://polygon-testnet-archive.allthatnode.com:8545', True)
    set_config('CHANNEL_ID', '1006453070189842472', True)
    set_config('DATABASE_URL', 'swan:swanDiscord@db:5432/swan', True)


def _load_env_file(env_file_path='.env'):
    if not os.path.isfile(env_file_path):
        error_logger.error(f'{env_file_path} does not exist.')
        raise FileNotFoundError(f'{env_file_path} does not exist.')
    load_dotenv(dotenv_path=env_file_path)


def get_env_from_file(key, env_file_path='.env'):
    _load_env_file(env_file_path)
    value = os.getenv(key)
    print(value)
    if value is None:
        error_logger.error(f'Environment variable {key} not found.')
        raise KeyError(f'Environment variable {key} not found.')
    return value


class ConfigManager:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ConfigManager.__instance is None:
            warning_logger.warning("A ConfigManager instance needs to be initialized first!")
            raise Exception("A ConfigManager instance needs to be initialized first!")
        return ConfigManager.__instance

    @classmethod
    async def create(cls, engine):
        self = ConfigManager()
        self.engine = engine
        self.config = await self.get_all_active_config()
        ConfigManager.__instance = self

        return self

    def __init__(self):
        """ Virtually private constructor. """
        if ConfigManager.__instance is not None:
            warning_logger.warning("This class is a singleton!")
            raise Exception("This class is a singleton!")

    async def get_all_active_config(self):
        async with self.engine.begin() as conn:
            try:
                query = get_all_active_config()
                config_dict = {}
                result = await conn.execute(query)
                for row in result.scalars():
                    print(row.key, row.value)
                    config_dict[row.key] = row.value
            except Exception as e:
                error_logger.error(f"Get all active config failed: {e}")
                exit(1)
        return config_dict

    def get_env(self, key):
        return str(self.config.get(key))
