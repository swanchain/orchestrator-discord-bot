# bot.py
import asyncio

import discord
from discord.ext.commands import Bot

from controller.bot_controller import BotController
from db.connection import connect_database
from db.session_manager import AsyncSessionManager
from log.logger import error_logger
from services.user_services import UserService
from model.config import get_config


async def main():
    engine = await connect_database()
    AsyncSessionManager(engine)
    intents = discord.Intents.all()
    client = Bot(command_prefix="$", intents=intents)
    bot_token = await get_config(key='BOT_TOKEN')
    print(bot_token)
    if bot_token is None or not isinstance(bot_token, str):
        error_logger.error(f"Bot token is not set or invalid")
        exit(1)
    user_service = UserService(engine)
    await BotController.create(client, user_service)

    try:
        await client.start(bot_token)
    except Exception as e:
        error_logger.error(f"Bot connection failed: {e}")
        exit(1)


asyncio.run(main())

# TODO: Update Readme file
