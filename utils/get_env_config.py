import os

from dotenv import load_dotenv
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
