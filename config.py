import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

DEFAULTS = {
    "rpc_url": "https://testnet-rpc.monad.xyz",
    "chain_id": 10143,
    "poll_interval": 5,
    "block_history": 20,
    "gas_price_multiplier": 1.1,
    "timeout": 30,
    "log_level": "INFO",
}


def load_config() -> dict:
    cfg = dict(DEFAULTS)
    if CONFIG_PATH.exists():
        try:
            with CONFIG_PATH.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            cfg.update(data)
        except (json.JSONDecodeError, OSError):
            pass
    return cfg


def save_config(cfg: dict) -> None:
    with CONFIG_PATH.open("w", encoding="utf-8") as fh:
        json.dump(cfg, fh, indent=2)


def interactive_setup() -> None:
    from rich.console import Console
    from rich.prompt import Prompt

    console = Console()
    cfg = load_config()

    console.print("[bold green]Monad BFT Configuration[/bold green]\n")
    console.print("Press Enter to keep current value.\n")

    cfg["rpc_url"] = Prompt.ask("RPC endpoint URL", default=cfg["rpc_url"])
    cfg["chain_id"] = int(Prompt.ask("Chain ID", default=str(cfg["chain_id"])))
    cfg["poll_interval"] = int(Prompt.ask("Monitor poll interval (seconds)", default=str(cfg["poll_interval"])))
    cfg["block_history"] = int(Prompt.ask("Block history depth", default=str(cfg["block_history"])))
    cfg["gas_price_multiplier"] = float(
        Prompt.ask("Gas price multiplier", default=str(cfg["gas_price_multiplier"]))
    )
    cfg["timeout"] = int(Prompt.ask("RPC timeout (seconds)", default=str(cfg["timeout"])))

    save_config(cfg)
    console.print("\n[bold green]Configuration saved.[/bold green]")
