import discord

from log.logger import info_logger, error_logger
from web3 import Web3
from model.config import get_config
from services.user_services import UserService
import asyncio


class BotController:
    def __init__(self, client, user_service: UserService):
        self.client = client
        self.user_service = user_service
        self.semaphore = None

    @classmethod
    async def create(cls, client, user_service: UserService):
        instance = cls(client, user_service)
        await instance.register_events()
        return instance

    async def register_events(self):
        max_request = await get_config('MAX_REQUEST')
        self.semaphore = asyncio.BoundedSemaphore(int(max_request))

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
                                     f'-- {guild.name} (id: {guild.id}) \n')
                else:
                    info_logger.info(f'-- {self.client.user} is not connected to any guilds.')
                    return
            except Exception as e:
                error_logger.error(f"Failed to get guild: {e}")
                return

        # @self.client.command(name='lag_faucet', help='Claim tokens from the faucet')
        # async def claim_polygon(ctx):
        #     await self._process_claim_request(ctx, 'POLYGON', 'LAG')

        @self.client.command(name='swan_faucet', help='Claim tokens from the faucet')
        async def claim_swan(ctx):
            await self._process_claim_request(ctx, 'SATURN', 'SWAN', True)

        # @self.client.command(name='swan_usdc_faucet', help='Claim tokens from the faucet')
        # async def claim_op(ctx):
        #     await self._process_claim_request(ctx, 'OPSWAN', 'OPSWAN_TEST_USDC', True)

    async def _process_claim_request(self, ctx, network, token_symbol, is_test=False):
        async with self.semaphore:
            channel_id = await get_config(f'{network}_CHANNEL_ID')
            if ctx.channel.id != int(channel_id):
                error_logger.error(f"Received invalid channel id: {ctx.channel.id}")
                await ctx.reply('Invalid channel id')
                return
            to_wallet_address = ctx.message.content.split()[-1]
            if to_wallet_address == '' or not Web3.is_address(to_wallet_address):
                error_logger.error(f"Invalid wallet address: {to_wallet_address}")
                await ctx.reply('Bot command must be in the format: $faucet <wallet_address>')
                return
            await ctx.reply(f'Your claim is being processed. Please wait...')
            from_wallet_address = await get_config('FROM_WALLET_ADDRESS')
            claimed_amount = await get_config('CLAIMED_AMOUNT')
            info_logger.info(f'-- {ctx.author} is claiming {claimed_amount} {token_symbol} to {to_wallet_address}')
            tx_hash = await self.user_service.transfer_and_record(ctx.author.id, ctx.author.name, network,
                                                                  from_wallet_address, to_wallet_address,
                                                                  int(claimed_amount), token_symbol, is_test)
            if tx_hash is None:
                await ctx.reply(
                    f'Failed to claim {claimed_amount} {token_symbol} to {to_wallet_address}, please try again later.')
            else:
                await ctx.reply(
                    f'Claimed {claimed_amount} {token_symbol} to {to_wallet_address}, your tx_hash is: {tx_hash}, '
                    f'you will receive it shortly.')
