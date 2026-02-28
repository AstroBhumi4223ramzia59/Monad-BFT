import logging
from typing import Optional

from web3 import Web3
from eth_account import Account

logger = logging.getLogger(__name__)


class TxBuilder:
    """Transaction builder for the Monad EVM.

    Provides methods to construct, sign, and broadcast transactions
    against a Monad JSON-RPC endpoint. Supports native transfers,
    contract calls, and gas estimation.
    """

    def __init__(self, config: dict) -> None:
        self.rpc_url = config.get("rpc_url", "")
        self.chain_id = config.get("chain_id", 10143)
        self.gas_multiplier = config.get("gas_price_multiplier", 1.1)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

    def get_nonce(self, address: str) -> int:
        return self.w3.eth.get_transaction_count(Web3.to_checksum_address(address))

    def estimate_gas(self, to: str, data: str = "0x", value: int = 0) -> int:
        tx = {
            "to": Web3.to_checksum_address(to),
            "data": data,
            "value": value,
        }
        return self.w3.eth.estimate_gas(tx)

    def send_native(self, private_key: str, to: str, amount_eth: float) -> str:
        account = Account.from_key(private_key)
        to_addr = Web3.to_checksum_address(to)
        value = self.w3.to_wei(amount_eth, "ether")

        nonce = self.w3.eth.get_transaction_count(account.address)
        gas_price = int(self.w3.eth.gas_price * self.gas_multiplier)

        tx = {
            "nonce": nonce,
            "to": to_addr,
            "value": value,
            "gas": 21000,
            "gasPrice": gas_price,
            "chainId": self.chain_id,
        }

        signed = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        return tx_hash.hex()

    def send_contract_call(
        self,
        private_key: str,
        to: str,
        data: str,
        value: int = 0,
        gas_limit: Optional[int] = None,
    ) -> str:
        account = Account.from_key(private_key)
        to_addr = Web3.to_checksum_address(to)
        nonce = self.w3.eth.get_transaction_count(account.address)
        gas_price = int(self.w3.eth.gas_price * self.gas_multiplier)

        if gas_limit is None:
            gas_limit = self.estimate_gas(to, data, value)
            gas_limit = int(gas_limit * 1.2)

        tx = {
            "nonce": nonce,
            "to": to_addr,
            "value": value,
            "gas": gas_limit,
            "gasPrice": gas_price,
            "data": data,
            "chainId": self.chain_id,
        }

        signed = self.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        return tx_hash.hex()
