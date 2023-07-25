import discord
from discord import Message
from log.logger import info_logger, error_logger
from web3 import Web3
from services.user_services import UserService
import config

BOT_TOKEN = config.get_env('BOT_TOKEN')
BOT_GUILD = config.get_env('BOT_GUILD')
WALLET_ADDRESS = config.get_env('WALLET_ADDRESS')
CLAIMED_AMOUNT = config.get_env('CLAIMED_AMOUNT')


class BotController:
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    def __init__(self, client, user_service: UserService):
        self.client = client
        self.user_service = user_service
        self.register_events()

    def register_events(self):
        @self.client.event
        async def on_ready():
            try:
                guild = discord.utils.get(self.client.guilds, name=BOT_GUILD)
                if guild is None:
                    info_logger.info(f'-- {self.client.user} is not connected to any guilds.')
                    return
                if isinstance(guild, discord.Guild):
                    info_logger.info(f'-- Logged on as {self.client.user}! \n'
                                     f'-- {self.client.user} is connected to the following guild: \n'
                                     f'-- {guild.name} (id: {guild.id})'
                                     )
                else:
                    info_logger.info(f'-- {self.client.user} is not connected to any guilds.')
                    return
            except Exception as e:
                error_logger.error(e, "Failed to get guild")
                return

        @self.client.event
        async def on_message(message: Message):
            if message.content.startswith('!claim'):
                args = message.content.split()
                if len(args) != 2:
                    await message.channel.send('Please provide your wallet address after !claim')
                    return
                wallet_address = args[1]
                if not Web3.is_address(wallet_address):
                    await message.channel.send('Invalid wallet address')
                    return
                from_wallet_address = WALLET_ADDRESS
                claimed_amount = CLAIMED_AMOUNT
                await self.user_service.transfer_and_record(message.author.id, message.author.name, from_wallet_address,
                                                            wallet_address, claimed_amount)
