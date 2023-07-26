from datetime import datetime

from sqlalchemy import insert
from web3 import Web3
from web3.middleware import geth_poa_middleware

import config
from log.logger import info_logger, error_logger
from model.user import users

PRIVATE_KEY = config.get_env('PRIVATE_KEY')
CONTRACT_ADDRESS = config.get_env('CONTRACT_ADDRESS')
RPC_ENDPOINT = config.get_env('RPC_ENDPOINT')


class UserService:
    def __init__(self, engine):
        self.engine = engine
        self.web3 = Web3(Web3.HTTPProvider(RPC_ENDPOINT))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.private_key = PRIVATE_KEY
        self.contract_address = CONTRACT_ADDRESS
        self.abi = [{
            "inputs": [
                {
                    "internalType": "address",
                    "name": "to",
                    "type": "address"
                },
                {
                    "internalType": "uint256",
                    "name": "amount",
                    "type": "uint256"
                }
            ],
            "name": "transfer",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "nonpayable",
            "type": "function"
        }]
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    async def _transfer(self, from_wallet_address, to_wallet_address, claimed_amount):
        claimed_amount = int(claimed_amount)
        if not self.web3.is_address(to_wallet_address) or not self.web3.is_address(from_wallet_address):
            error_logger.error(f'Invalid wallet address. From: {from_wallet_address}, To: {to_wallet_address}')
            return

        account = self.web3.eth.account.from_key(self.private_key)
        nonce = self.web3.eth.get_transaction_count(account.address)
        try:
            info_logger.info(
                f'-- Transferring {claimed_amount} LAD tokens to {to_wallet_address} at {datetime.utcnow()}')
            tx = self.contract.functions.transfer(to_wallet_address, claimed_amount).build_transaction({
                'from': from_wallet_address,
                'gas': 100000,
                'gasPrice': self.web3.to_wei('10', 'gwei'),
                'nonce': nonce,
            })
            signed_tx = account.sign_transaction(tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)

            # Wait for the transaction to be mined, and get the transaction receipt
            txn_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception as e:
            error_logger.error(f"Failed to transfer to {to_wallet_address} at {datetime.utcnow()}, error: {e}")
            raise

        info_logger.info(f'-- Transaction successful with transaction hash: {tx_hash.hex()} at {datetime.utcnow()}')
        info_logger.info(f'-- Transaction receipt: {txn_receipt}')
        info_logger.info(
            f'-- Gas used: {txn_receipt["gasUsed"]} for transaction hash: {tx_hash.hex()} at {datetime.utcnow()}')
        return tx_hash.hex()

    async def _record_user_transaction(self, discord_id, discord_name, from_wallet_address, to_wallet_address,
                                       claimed_amount, tx_hash):
        async with self.engine.begin() as conn:
            info_logger.info(f'-- Recording transaction for {discord_name} at {datetime.utcnow()}...')
            try:
                query = insert(users).values(discord_id=str(discord_id),
                                             discord_name=discord_name,
                                             from_wallet_address=from_wallet_address,
                                             to_wallet_address=to_wallet_address,
                                             last_claim_time=datetime.utcnow(),
                                             claimed_amount=float(claimed_amount),
                                             transaction_hash=str(tx_hash)
                                             )
                await conn.execute(query)
                info_logger.info(f'-- Transaction recorded for {discord_name} at {datetime.utcnow()}')
            except Exception as e:
                error_logger.error(f"Failed to insert transaction: {e}")
                raise

    async def transfer_and_record(self, discord_id, discord_name, from_wallet_address, to_wallet_address,
                                  claimed_amount):
        try:
            tx_hash = await self._transfer(from_wallet_address, to_wallet_address, claimed_amount)

            await self._record_user_transaction(discord_id, discord_name, from_wallet_address, to_wallet_address,
                                                claimed_amount, tx_hash)
            return tx_hash
        except Exception as e:
            error_logger.error(f"Failed to transfer and record transaction: {e}")
            raise
