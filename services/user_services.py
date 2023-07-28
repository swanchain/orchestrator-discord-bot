from datetime import datetime

from web3 import Web3
from web3.middleware import geth_poa_middleware

from log.logger import info_logger, error_logger
from model.user import set_user_claim_info
from db.init_database import config_manager


class UserService:
    def __init__(self, engine):
        self.private_key = config_manager.get_env('PRIVATE_KEY')
        self.contract_address = config_manager.get_env('CONTRACT_ADDRESS')
        self.rpc_endpoint = config_manager.get_env('RPC_ENDPOINT')
        self.engine = engine
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_endpoint))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.private_key = self.private_key
        self.contract_address = self.contract_address
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
        }, {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "account",
                    "type": "address"
                }
            ],
            "name": "balanceOf",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "",
                    "type": "uint256"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }]
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    async def _transfer(self, from_wallet_address, to_wallet_address, claimed_amount):
        if self.contract is None:
            error_logger.error(f'Contract is None')
            return None
        if not self.web3.is_address(to_wallet_address) or not self.web3.is_address(from_wallet_address):
            error_logger.error(f'Invalid wallet address. From: {from_wallet_address}, To: {to_wallet_address}')
            return None
        if not self.web3.is_connected():
            error_logger.error(f'Web3 is not connected')
            return None

        # check if the wallet has enough balance
        balance = self.contract.functions.balanceOf(from_wallet_address).call()
        if balance < claimed_amount:
            error_logger.error(f'Insufficient balance. Balance: {balance}, Claimed amount: {claimed_amount}')
            return None

        # check if the wallet has enough gas
        gas_price = self.web3.eth.gas_price
        gas = self.contract.functions.transfer(to_wallet_address, claimed_amount).estimate_gas({
            'from': from_wallet_address,
            'gasPrice': gas_price,
        })
        gas_cost = gas * gas_price
        if gas_cost > self.web3.eth.get_balance(from_wallet_address):
            error_logger.error(
                f'Insufficient gas. Gas: {gas_cost}, Balance: {self.web3.eth.get_balance(from_wallet_address)}')
            return None

        account = self.web3.eth.account.from_key(self.private_key)
        nonce = self.web3.eth.get_transaction_count(account.address)

        try:
            info_logger.info(
                f'-- Transferring {claimed_amount} LAD tokens to {to_wallet_address} at {datetime.utcnow()}')
            tx = self.contract.functions.transfer(to_wallet_address, claimed_amount).build_transaction({
                'from': from_wallet_address,
                'gas': gas,
                'gasPrice': gas_price,
                'nonce': nonce,
            })
            signed_tx = account.sign_transaction(tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            # Wait for the transaction to be mined, and get the transaction receipt
            txn_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception as e:
            error_logger.error(f"Failed to transfer to {to_wallet_address} at {datetime.utcnow()}, error: {e}")
            return None

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
                query = set_user_claim_info(str(discord_id), discord_name, from_wallet_address, to_wallet_address,
                                            claimed_amount, tx_hash)
                await conn.execute(query)
                info_logger.info(f'-- Transaction recorded for {discord_name} at {datetime.utcnow()}')
                return True
            except Exception as e:
                error_logger.error(f"Failed to insert transaction: {e}")
                return False

    async def transfer_and_record(self, discord_id, discord_name, from_wallet_address, to_wallet_address,
                                  claimed_amount):
        claimed_amount = self.web3.to_wei(int(claimed_amount), 'ether')

        tx_hash = await self._transfer(from_wallet_address, to_wallet_address, claimed_amount)
        if not tx_hash:
            return None

        is_success = await self._record_user_transaction(discord_id, discord_name, from_wallet_address,
                                                         to_wallet_address,
                                                         claimed_amount, tx_hash)
        if not is_success:
            return None
        return tx_hash
