# bot.py
import asyncio

import discord
from discord.ext.commands import Bot

from controller.bot_controller import BotController
from db import connection, init_database
from log.logger import error_logger

import config
from services.user_services import UserService

BOT_TOKEN = config.get_env('BOT_TOKEN')
BOT_GUILD = config.get_env('BOT_GUILD')


async def main():
    init_database.create_table()
    intents = discord.Intents.all()
    client = Bot(command_prefix="$", intents=intents)
    engine = await connection.connect_database()
    user_service = UserService(engine)
    BotController(client, user_service)

    try:
        await client.start(BOT_TOKEN)
    except Exception as e:
        error_logger.error(f"Bot connection failed: {e}")
        exit(1)


asyncio.run(main())

# TODO: Update Readme file
