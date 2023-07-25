# bot.py
import discord

from controller.bot_controller import BotController
from db.connection import engine
from log.logger import info_logger, error_logger

import config
from services.user_services import UserService

BOT_TOKEN = config.get_env('BOT_TOKEN')
BOT_GUILD = config.get_env('BOT_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
user_service = UserService(engine)
bot_controller = BotController(client, user_service)

try:
    client.run(BOT_TOKEN)
except Exception as e:
    error_logger.error(e, "Bot connection failed")
    exit(1)