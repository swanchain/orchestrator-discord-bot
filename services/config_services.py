import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import select, Engine
from sqlalchemy.orm import sessionmaker
from log.logger import error_logger
from model.config import Config


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
    def __init__(self, engine: Engine):
        self.engine = engine
        self.session = sessionmaker(self.engine)
        self.set_all_config()

    def get_all_active_config(self) -> dict:
        with self.session() as session:
            try:
                config_dict = {}
                for row in session.execute(select(Config).where(Config.is_active == True)):
                    config_obj = row[0]
                    config_dict[config_obj.key] = config_obj.value
            except Exception as e:
                error_logger.error(f"Get all active config failed: {e}")
                exit(1)
        return config_dict

    def get_env(self, key):
        config_dist = self.get_all_active_config()
        return str(config_dist.get(key))

    def set_all_config(self):
        session = self.session()
        try:
            session.merge(
                Config(key='BOT_TOKEN',
                       value='MTEzMzU5Nzc4MTExNDc2OTQ5MA.GxTU1m.CAIZnG6SHmaHm4m3HI421TKdx6QcRkJ4XvNlX0',
                       is_active=True))
            session.merge(Config(key='BOT_GUILD', value='PTS', is_active=True))
            session.merge(
                Config(key='FROM_WALLET_ADDRESS', value='0x29eD49c8E973696D07E7927f748F6E5Eacd5516D',
                       is_active=True))
            session.merge(Config(key='CLAIMED_AMOUNT', value='1500', is_active=True))
            session.merge(
                Config(key='PRIVATE_KEY',
                       value='895bcb462f77386e68b726666ee9a026ad87078086aa0e5c64f681a090c8265a',
                       is_active=True))
            session.merge(
                Config(key='CONTRACT_ADDRESS', value='0x3CF24790B3af64029564E81B67aF299dB83Fd9e3',
                       is_active=True))
            session.merge(
                Config(key='RPC_ENDPOINT', value='https://polygon-testnet-archive.allthatnode.com:8545',
                       is_active=True))
            session.merge(Config(key='CHANNEL_ID', value='1133939349763915876', is_active=True))
            session.commit()

        except Exception as e:
            error_logger.error(f'-- Failed to set config at {datetime.utcnow()}: {e}')
            session.rollback()
            raise e
        finally:
            session.close()
