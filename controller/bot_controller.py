import discord

from log.logger import info_logger, error_logger
from web3 import Web3
from services.user_services import UserService
import config

BOT_GUILD = config.get_env('BOT_GUILD')
FROM_WALLET_ADDRESS = config.get_env('FROM_WALLET_ADDRESS')
CLAIMED_AMOUNT = config.get_env('CLAIMED_AMOUNT')
CHANNEL_ID = config.get_env('CHANNEL_ID')


class BotController:
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
            if ctx.channel.id != int(CHANNEL_ID):
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
            from_wallet_address = FROM_WALLET_ADDRESS
            claimed_amount = CLAIMED_AMOUNT
            info_logger.info(f'-- {ctx.author} is claiming {claimed_amount} tokens to {to_wallet_address}')
            tx_hash = await self.user_service.transfer_and_record(ctx.author.id, ctx.author.name, from_wallet_address,
                                                                  to_wallet_address, claimed_amount)
            if tx_hash is None:
                await ctx.reply(
                    f'Failed to claim {claimed_amount} tokens to {to_wallet_address}, please try again later.')
            else:
                await ctx.reply(
                    f'Claimed {claimed_amount} tokens to {to_wallet_address}, your tx_hash is: {tx_hash}, '
                    f'you will receive it shortly.')
