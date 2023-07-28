import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import select, Engine
from sqlalchemy.orm import sessionmaker
from log.logger import error_logger



def _load_env_file(env_file_path='.env'):
    if not os.path.isfile(env_file_path):
        error_logger.error(f'{env_file_path} does not exist.')
        raise FileNotFoundError(f'{env_file_path} does not exist.')
    load_dotenv(dotenv_path=env_file_path)


def get_env_from_file(key, env_file_path='.env'):
    _load_env_file(env_file_path)
    value = os.getenv(key)
    if value is None:
        error_logger.error(f'Environment variable {key} not found.')
        raise KeyError(f'Environment variable {key} not found.')
    return value



# class ConfigManager:
#     def __init__(self, engine: Engine):
#         self.engine = engine
#         self.session = sessionmaker(self.engine)
#         # self.set_all_config()
#
#     def get_all_active_config(self) -> dict:
#         with self.session() as session:
#             try:
#                 config_dict = {}
#                 for row in session.execute(select(Config).where(Config.is_active == True)):
#                     config_obj = row[0]
#                     config_dict[config_obj.key] = config_obj.value
#             except Exception as e:
#                 error_logger.error(f"Get all active config failed: {e}")
#                 exit(1)
#             finally:
#                 session.close()
#         return config_dict
#
#     def get_env(self, key):
#         config_dist = self.get_all_active_config()
#         return str(config_dist.get(key))
#
#     # def set_all_config(self):
#     #     session = self.session()
#     #     try:
#     #         session.merge(
#     #             Config(key='BOT_TOKEN',
#     #                    value='bot_token(str)',
#     #                    is_active=True))
#     #         session.merge(Config(key='BOT_GUILD', value='bot_guild(str)', is_active=True))
#     #         session.merge(
#     #             Config(key='FROM_WALLET_ADDRESS', value='from_wallet_address(str)',
#     #                    is_active=True))
#     #         session.merge(Config(key='CLAIMED_AMOUNT', value='claimed_amount(int)', is_active=True))
#     #         session.merge(
#     #             Config(key='PRIVATE_KEY',
#     #                    value='private_key(str)',
#     #                    is_active=True))
#     #         session.merge(
#     #             Config(key='CONTRACT_ADDRESS', value='contract_address(str)',
#     #                    is_active=True))
#     #         session.merge(
#     #             Config(key='RPC_ENDPOINT', value='rpc_endpoint(str)',
#     #                    is_active=True))
#     #         session.merge(Config(key='CHANNEL_ID', value='channel_id(int)', is_active=True))
#     #         session.commit()
#     #
#     #     except Exception as e:
#     #         error_logger.error(f'-- Failed to set config at {datetime.utcnow()}: {e}')
#     #         session.rollback()
#     #         raise e
#     #     finally:
#     #         session.close()

