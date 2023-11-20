from datetime import datetime

from web3 import Web3
from model.config import get_config
from log.logger import info_logger, error_logger
from model.user import set_user_claim_info


class UserService:
    def __init__(self, engine):
        self.engine = engine
        self.common_abi = [{
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

    async def _transfer(self, network, token_name, from_wallet_address, to_wallet_address, claimed_amount, is_test=False):
        rpc_endpoint_key = f'{network}_{"TEST_" if is_test else ""}RPC_ENDPOINT'
        web3 = Web3(Web3.HTTPProvider(await get_config(rpc_endpoint_key)))
        print(await get_config(rpc_endpoint_key))

        contract_key = f'{token_name}_{"TEST_" if is_test else ""}CONTRACT_ADDRESS'
        contract_address = await get_config(contract_key)
        contract = web3.eth.contract(address=contract_address, abi=self.common_abi)
        if contract is None:
            error_logger.error(f'Contract is None')
            return None
        if not web3.is_address(to_wallet_address) or not web3.is_address(from_wallet_address):
            error_logger.error(f'Invalid wallet address. From: {from_wallet_address}, To: {to_wallet_address}')
            return None
        if not web3.is_connected():
            error_logger.error(f'Web3 is not connected')
            return None

        # check if the wallet has enough balance
        balance = contract.functions.balanceOf(from_wallet_address).call()
        if balance < claimed_amount:
            error_logger.error(f'Insufficient balance. Balance: {balance}, Claimed amount: {claimed_amount}')
            return None

        # check if the wallet has enough gas
        gas_price = web3.eth.gas_price
        gas = contract.functions.transfer(to_wallet_address, claimed_amount).estimate_gas({
            'from': from_wallet_address,
            'gasPrice': gas_price,
        })
        gas_cost = gas * gas_price
        if gas_cost > web3.eth.get_balance(from_wallet_address):
            error_logger.error(
                f'Insufficient gas. Gas: {gas_cost}, Balance: {web3.eth.get_balance(from_wallet_address)}')
            return None

        private_key = await get_config('PRIVATE_KEY')
        account = web3.eth.account.from_key(private_key)
        nonce = web3.eth.get_transaction_count(account.address)

        try:
            info_logger.info(
                f'-- Transferring {claimed_amount} tokens to {to_wallet_address} at {datetime.utcnow()}')
            tx = contract.functions.transfer(to_wallet_address, claimed_amount).build_transaction({
                'from': from_wallet_address,
                'gas': gas,
                'gasPrice': gas_price,
                'nonce': nonce,
            })
            signed_tx = account.sign_transaction(tx)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            # Wait for the transaction to be mined, and get the transaction receipt
            txn_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception as e:
            error_logger.error(f"Failed to transfer to {to_wallet_address} at {datetime.utcnow()}, error: {e}")
            return None

        info_logger.info(f'-- Transaction successful with transaction hash: {tx_hash.hex()} at {datetime.utcnow()}')
        info_logger.info(f'-- Transaction receipt: {txn_receipt}')
        info_logger.info(
            f'-- Gas used: {txn_receipt["gasUsed"]} for transaction hash: {tx_hash.hex()} at {datetime.utcnow()}')
        return tx_hash.hex()

    async def _record_user_transaction(self, discord_id, discord_name, from_wallet_address, to_wallet_address,
                                       claimed_amount, tx_hash, token_symbol):
        async with self.engine.begin() as conn:
            info_logger.info(f'-- Recording transaction for {discord_name} at {datetime.utcnow()}...')
            try:
                query = set_user_claim_info(str(discord_id), discord_name, from_wallet_address, to_wallet_address,
                                            float(claimed_amount), tx_hash, token_symbol)
                await conn.execute(query)
                info_logger.info(f'-- Transaction recorded for {discord_name} at {datetime.utcnow()}')
                return True
            except Exception as e:
                error_logger.error(f"Failed to insert transaction: {e}")
                return False

    async def transfer_and_record(self, discord_id, discord_name, network, token_name, from_wallet_address, to_wallet_address,
                                  claimed_amount, token_symbol, is_test=False):
        web3 = Web3(Web3.HTTPProvider(await get_config(f'{network}_{"TEST_" if is_test else ""}RPC_ENDPOINT')))
        if token_name == 'OPSWAN' or token_name == 'POLYGON_USDC':
            claimed_amount = web3.to_wei(claimed_amount, 'mwei')
        else:
            claimed_amount = web3.to_wei(claimed_amount, 'ether')

        tx_hash = await self._transfer(network, token_name, from_wallet_address, to_wallet_address, claimed_amount, is_test)
        if not tx_hash:
            return None

        is_success = await self._record_user_transaction(discord_id, discord_name, from_wallet_address,
                                                         to_wallet_address, claimed_amount, tx_hash, token_symbol)
        if not is_success:
            return None
        return tx_hash

