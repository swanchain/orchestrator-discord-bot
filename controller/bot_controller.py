import discord

from log.logger import info_logger, error_logger
from web3 import Web3
from model.config import get_config
# from db.init_database import config_manager
from services.user_services import UserService
import asyncio


class BotController:
    def __init__(self, client, user_service: UserService):
        self.client = client
        self.user_service = user_service

    @classmethod
    async def create(cls, client, user_service: UserService):
        instance = cls(client, user_service)
        await instance.register_events()
        return instance

    async def register_events(self):
        max_request = await get_config('MAX_REQUEST')
        semaphore = asyncio.BoundedSemaphore(int(max_request))

        @self.client.event
        async def on_ready():
            try:
                bot_guild = await get_config('BOT_GUILD')
                guild = discord.utils.get(self.client.guilds, name=bot_guild)
                if guild is None:
                    info_logger.info(f'-- {self.client.user} is not connected to any guilds.')
                    return
                if isinstance(guild, discord.Guild):
                    info_logger.info(f'-- Logged on as {self.client.user}! \n'
                                     f'-- {self.client.user} is connected to the following guild: \n'
                                     f'-- {guild.name} (id: {guild.id}) \n'
                                     )
                else:
                    info_logger.info(f'-- {self.client.user} is not connected to any guilds.')
                    return
            except Exception as e:
                error_logger.error(f"Failed to get guild: {e}")
                return

        @self.client.command(name='faucet', help='Claim tokens from the faucet')
        async def claim(ctx, to_wallet_address: str = ''):
            async with semaphore:
                channel_id = await get_config('CHANNEL_ID')
                if ctx.channel.id != int(channel_id):
                    error_logger.error(f"Received invalid channel id: {ctx.channel.id}")
                    await ctx.reply('Invalid channel id')
                    return
                if to_wallet_address == '':
                    error_logger.error(f"Received empty wallet address")
                    await ctx.reply('Bot command must be in the format: $faucet <wallet_address>')
                    return
                if not Web3.is_address(to_wallet_address):
                    error_logger.error(f"Received invalid wallet address: {to_wallet_address}")
                    await ctx.reply('Invalid wallet address')
                    return
                await ctx.reply(f'Your claim is being processed. Please wait...')
                from_wallet_address = await get_config('FROM_WALLET_ADDRESS')
                claimed_amount = await get_config('CLAIMED_AMOUNT')
                info_logger.info(f'-- {ctx.author} is claiming {claimed_amount} LAG to {to_wallet_address}')
                tx_hash = await self.user_service.transfer_and_record(ctx.author.id, ctx.author.name,
                                                                      from_wallet_address,
                                                                      to_wallet_address, int(claimed_amount), 'LAG')
                if tx_hash is None:
                    await ctx.reply(
                        f'Failed to claim {claimed_amount} LAG to {to_wallet_address}, please try again later.')
                else:
                    await ctx.reply(
                        f'Claimed {claimed_amount} LAG to {to_wallet_address}, your tx_hash is: {tx_hash}, '
                        f'you will receive it shortly.')
