import logging
from typing import Optional

import requests
from rich.console import Console
from rich.table import Table
from rich import box

logger = logging.getLogger(__name__)


class BlockExplorer:
    """Lightweight block and transaction explorer via JSON-RPC.

    Queries the Monad RPC endpoint to retrieve block headers,
    transaction details, and receipts.
    """

    def __init__(self, config: dict) -> None:
        self.rpc_url = config.get("rpc_url", "")
        self.timeout = config.get("timeout", 30)
        self.console = Console()

    def _rpc_call(self, method: str, params: list = None) -> Optional[dict]:
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": 1,
        }
        try:
            resp = requests.post(self.rpc_url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            result = resp.json()
            if "error" in result:
                logger.error("RPC error: %s", result["error"])
                return None
            return result.get("result")
        except requests.RequestException as exc:
            logger.error("RPC request failed: %s", exc)
            return None

    def get_latest_block(self) -> Optional[dict]:
        return self._rpc_call("eth_getBlockByNumber", ["latest", True])

    def get_block_by_number(self, number: int) -> Optional[dict]:
        return self._rpc_call("eth_getBlockByNumber", [hex(number), True])

    def get_transaction(self, tx_hash: str) -> Optional[dict]:
        return self._rpc_call("eth_getTransactionByHash", [tx_hash])

    def get_transaction_receipt(self, tx_hash: str) -> Optional[dict]:
        return self._rpc_call("eth_getTransactionReceipt", [tx_hash])

    def print_block(self, block: dict) -> None:
        table = Table(
            title="[bold green]Block Details[/bold green]",
            box=box.ROUNDED,
            border_style="green",
        )
        table.add_column("Field", style="bold white")
        table.add_column("Value", style="bright_green")

        number = int(block.get("number", "0x0"), 16)
        timestamp = int(block.get("timestamp", "0x0"), 16)
        gas_used = int(block.get("gasUsed", "0x0"), 16)
        gas_limit = int(block.get("gasLimit", "0x0"), 16)
        tx_count = len(block.get("transactions", []))

        table.add_row("Number", f"{number:,}")
        table.add_row("Hash", block.get("hash", "N/A"))
        table.add_row("Parent Hash", block.get("parentHash", "N/A"))
        table.add_row("Timestamp", str(timestamp))
        table.add_row("Miner", block.get("miner", "N/A"))
        table.add_row("Gas Used", f"{gas_used:,}")
        table.add_row("Gas Limit", f"{gas_limit:,}")
        table.add_row("Transactions", str(tx_count))
        table.add_row("State Root", block.get("stateRoot", "N/A"))

        self.console.print(table)

    def print_transaction(self, tx: dict) -> None:
        table = Table(
            title="[bold green]Transaction Details[/bold green]",
            box=box.ROUNDED,
            border_style="green",
        )
        table.add_column("Field", style="bold white")
        table.add_column("Value", style="bright_green")

        value_wei = int(tx.get("value", "0x0"), 16)
        gas = int(tx.get("gas", "0x0"), 16)
        gas_price = int(tx.get("gasPrice", "0x0"), 16)

        table.add_row("Hash", tx.get("hash", "N/A"))
        table.add_row("From", tx.get("from", "N/A"))
        table.add_row("To", tx.get("to", "N/A") or "Contract Creation")
        table.add_row("Value (wei)", f"{value_wei:,}")
        table.add_row("Gas", f"{gas:,}")
        table.add_row("Gas Price (wei)", f"{gas_price:,}")
        table.add_row("Nonce", str(int(tx.get("nonce", "0x0"), 16)))
        table.add_row("Block", str(int(tx.get("blockNumber", "0x0"), 16)))
        table.add_row("Input (first 66 chars)", tx.get("input", "0x")[:66])

        self.console.print(table)
