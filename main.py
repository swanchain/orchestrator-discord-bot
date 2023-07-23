# bot.py
import discord
from log.logger import info_logger, error_logger

import config

BOT_TOKEN = config.get_env('BOT_TOKEN')
BOT_GUILD = config.get_env('BOT_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    try:
        guild = discord.utils.get(client.guilds, name=BOT_GUILD)
        if guild is None:
            info_logger.info(
                f'-- {client.user} is not connected to any guilds.'
            )
            return
        info_logger.info(f'-- Logged on as {client.user}! \n'
                         f'-- {client.user} is connected to the following guild: \n'
                         f'-- {guild.name} (id: {guild.id})'
                         )
    except Exception as e:
        error_logger.error(e, "Failed to get guild")
        return


try:
    client.run(BOT_TOKEN)
except Exception as e:
    error_logger.error(e, "Bot connection failed")
    exit(1)