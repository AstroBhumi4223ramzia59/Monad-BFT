import logging
import time
from typing import Optional

import requests
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich import box

logger = logging.getLogger(__name__)


class MonadMonitor:
    """Real-time node monitor for Monad BFT networks.

    Polls the JSON-RPC endpoint to track block height, peer count,
    gas prices, and consensus round information. Renders a live
    dashboard using Rich.
    """

    def __init__(self, config: dict) -> None:
        self.rpc_url = config.get("rpc_url", "")
        self.poll_interval = config.get("poll_interval", 5)
        self.timeout = config.get("timeout", 30)
        self.console = Console()
        self._last_block: Optional[int] = None
        self._blocks_seen = 0
        self._start_time = 0.0

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
            return resp.json()
        except requests.RequestException as exc:
            logger.debug("RPC call %s failed: %s", method, exc)
            return None

    def _get_block_number(self) -> Optional[int]:
        data = self._rpc_call("eth_blockNumber")
        if data and "result" in data:
            return int(data["result"], 16)
        return None

    def _get_gas_price(self) -> Optional[int]:
        data = self._rpc_call("eth_gasPrice")
        if data and "result" in data:
            return int(data["result"], 16)
        return None

    def _get_peer_count(self) -> Optional[int]:
        data = self._rpc_call("net_peerCount")
        if data and "result" in data:
            return int(data["result"], 16)
        return None

    def _get_chain_id(self) -> Optional[int]:
        data = self._rpc_call("eth_chainId")
        if data and "result" in data:
            return int(data["result"], 16)
        return None

    def _get_syncing(self) -> Optional[dict]:
        data = self._rpc_call("eth_syncing")
        if data and "result" in data:
            return data["result"]
        return None

    def _build_dashboard(self) -> Table:
        block_num = self._get_block_number()
        gas_price = self._get_gas_price()
        peer_count = self._get_peer_count()
        chain_id = self._get_chain_id()
        syncing = self._get_syncing()

        if block_num is not None:
            if self._last_block is not None and block_num > self._last_block:
                self._blocks_seen += block_num - self._last_block
            self._last_block = block_num

        elapsed = time.time() - self._start_time if self._start_time else 0
        bps = self._blocks_seen / elapsed if elapsed > 0 else 0.0

        sync_status = "synced"
        if isinstance(syncing, dict):
            current = int(syncing.get("currentBlock", "0x0"), 16)
            highest = int(syncing.get("highestBlock", "0x0"), 16)
            sync_status = f"syncing ({current}/{highest})"

        table = Table(
            title="[bold green]Monad BFT Node Monitor[/bold green]",
            box=box.ROUNDED,
            border_style="green",
            expand=True,
        )
        table.add_column("Metric", style="bold white", min_width=20)
        table.add_column("Value", style="bright_green", min_width=30)

        table.add_row("RPC Endpoint", self.rpc_url)
        table.add_row("Chain ID", str(chain_id) if chain_id else "N/A")
        table.add_row("Block Height", f"{block_num:,}" if block_num else "N/A")
        table.add_row("Gas Price", f"{gas_price:,} wei" if gas_price else "N/A")
        table.add_row("Gas Price (Gwei)", f"{gas_price / 1e9:.4f}" if gas_price else "N/A")
        table.add_row("Peer Count", str(peer_count) if peer_count is not None else "N/A")
        table.add_row("Sync Status", sync_status)
        table.add_row("Blocks/sec", f"{bps:.2f}")
        table.add_row("Uptime", f"{elapsed:.0f}s")

        return table

    def run(self) -> None:
        self._start_time = time.time()
        self._blocks_seen = 0
        self._last_block = None

        self.console.print(
            "[dim]Press Ctrl+C to stop monitoring.[/dim]\n"
        )

        with Live(self._build_dashboard(), refresh_per_second=1, console=self.console) as live:
            while True:
                time.sleep(self.poll_interval)
                live.update(self._build_dashboard())
