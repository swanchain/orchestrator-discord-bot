# logger.py
import logging
import os

if not os.path.exists('./logs'):
    os.makedirs('logs')

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

info_logger = logging.getLogger('info')
info_handler = logging.FileHandler('logs/info.log')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
info_logger.addHandler(info_handler)

warning_logger = logging.getLogger('warning')
warning_handler = logging.FileHandler('logs/warning.log')
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
warning_logger.addHandler(warning_handler)

error_logger = logging.getLogger('error')
error_handler = logging.FileHandler('logs/error.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
error_logger.addHandler(error_handler)
