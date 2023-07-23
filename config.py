from dotenv import load_dotenv
import os

load_dotenv()


def get_env(key):
    return os.getenv(key)
