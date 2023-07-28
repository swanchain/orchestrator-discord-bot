# bot.py
import asyncio

import discord
from discord.ext.commands import Bot

from controller.bot_controller import BotController
from db import connection, init_database
from log.logger import error_logger
from services.user_services import UserService
from model.config import get_config


async def main():
    # init_database.create_table()
    engine = await connection.connect_database()
    intents = discord.Intents.all()
    client = Bot(command_prefix="$", intents=intents)
    bot_token = get_config(key='BOT_TOKEN')
    user_service = UserService(engine)
    BotController(client, user_service)

    try:
        await client.start(bot_token)
    except Exception as e:
        error_logger.error(f"Bot connection failed: {e}")
        exit(1)


asyncio.run(main())

# TODO: Update Readme file
