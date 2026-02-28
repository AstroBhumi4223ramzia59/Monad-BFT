import os
import subprocess
import sys
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from utils import ensure_env

BASE_DIR = Path(__file__).resolve().parent
REQUIREMENTS_PATH = BASE_DIR / "requirements.txt"

console = Console()

LOGO = r"""
 ███╗   ███╗ ██████╗ ███╗   ██╗ █████╗ ██████╗
 ████╗ ████║██╔═══██╗████╗  ██║██╔══██╗██╔══██╗
 ██╔████╔██║██║   ██║██╔██╗ ██║███████║██║  ██║
 ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══██║██║  ██║
 ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║  ██║██████╔╝
 ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝
      BFT Network Toolkit
"""


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_logo() -> None:
    console.print(
        Panel.fit(
            LOGO,
            border_style="bright_green",
            style="bold green",
            padding=(0, 2),
        )
    )


def run_pip_install() -> None:
    clear_screen()
    print_logo()

    if not REQUIREMENTS_PATH.exists():
        console.print("[bold red]requirements.txt not found.[/bold red]")
        input("\nPress Enter to return...")
        return

    console.print(
        Panel(
            "[bold yellow]Installing dependencies...[/bold yellow]\n"
            f"[dim]{REQUIREMENTS_PATH}[/dim]",
            border_style="yellow",
        )
    )

    cmd = [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_PATH)]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        assert proc.stdout is not None
        for line in proc.stdout:
            console.print(line.rstrip())
        ret = proc.wait()
        if ret == 0:
            console.print("\n[bold green]Dependencies installed successfully.[/bold green]")
        else:
            console.print(f"\n[bold red]pip exited with code {ret}.[/bold red]")
    except FileNotFoundError:
        console.print("[bold red]Failed to locate pip.[/bold red]")

    input("\nPress Enter to return...")


def configure_settings() -> None:
    from config import interactive_setup
    clear_screen()
    print_logo()
    interactive_setup()
    input("\nPress Enter to return...")


def run_node_monitor() -> None:
    clear_screen()
    print_logo()

    try:
        from monitor import MonadMonitor
        from config import load_config
    except ImportError as exc:
        console.print(f"[bold red]Import error:[/bold red] {exc}")
        input("\nPress Enter to return...")
        return

    cfg = load_config()
    mon = MonadMonitor(cfg)

    console.print(
        Panel(
            "[bold yellow]Starting Node Monitor[/bold yellow]\n\n"
            f"RPC endpoint: {cfg.get('rpc_url', 'N/A')}\n"
            f"Poll interval: {cfg.get('poll_interval', 5)}s",
            border_style="yellow",
        )
    )

    try:
        mon.run()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Monitor stopped.[/bold yellow]")
    except Exception as exc:
        console.print(f"[bold red]Monitor error:[/bold red] {exc}")

    input("\nPress Enter to return...")


def transaction_tools() -> None:
    clear_screen()
    print_logo()

    try:
        from tools.tx_builder import TxBuilder
        from config import load_config
    except ImportError as exc:
        console.print(f"[bold red]Import error:[/bold red] {exc}")
        input("\nPress Enter to return...")
        return

    cfg = load_config()
    builder = TxBuilder(cfg)

    console.print(
        Panel(
            "[bold cyan]Transaction Tools[/bold cyan]\n\n"
            "Build, sign, and broadcast transactions on the Monad EVM.",
            border_style="cyan",
        )
    )

    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    table.add_row("[bold green][1][/bold green]", "Send native transfer")
    table.add_row("[bold green][2][/bold green]", "Estimate gas for a call")
    table.add_row("[bold green][3][/bold green]", "Get nonce for address")
    table.add_row("[bold green][0][/bold green]", "Back")
    console.print(table)

    choice = Prompt.ask("Select", choices=["0", "1", "2", "3"], default="0")

    if choice == "1":
        to_addr = Prompt.ask("Recipient address")
        amount = Prompt.ask("Amount (ETH)", default="0.01")
        pk = Prompt.ask("Private key (hex)")
        try:
            tx_hash = builder.send_native(pk, to_addr, float(amount))
            console.print(f"[bold green]Transaction sent:[/bold green] {tx_hash}")
        except Exception as exc:
            console.print(f"[bold red]Error:[/bold red] {exc}")
    elif choice == "2":
        to_addr = Prompt.ask("Target address")
        data = Prompt.ask("Call data (hex)", default="0x")
        try:
            gas = builder.estimate_gas(to_addr, data)
            console.print(f"[bold green]Estimated gas:[/bold green] {gas}")
        except Exception as exc:
            console.print(f"[bold red]Error:[/bold red] {exc}")
    elif choice == "3":
        addr = Prompt.ask("Address")
        try:
            nonce = builder.get_nonce(addr)
            console.print(f"[bold green]Nonce:[/bold green] {nonce}")
        except Exception as exc:
            console.print(f"[bold red]Error:[/bold red] {exc}")

    input("\nPress Enter to return...")


def block_explorer() -> None:
    clear_screen()
    print_logo()

    try:
        from tools.explorer import BlockExplorer
        from config import load_config
    except ImportError as exc:
        console.print(f"[bold red]Import error:[/bold red] {exc}")
        input("\nPress Enter to return...")
        return

    cfg = load_config()
    explorer = BlockExplorer(cfg)

    console.print(
        Panel(
            "[bold cyan]Block Explorer[/bold cyan]\n\n"
            "Query blocks and transactions via the Monad RPC endpoint.",
            border_style="cyan",
        )
    )

    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    table.add_row("[bold green][1][/bold green]", "Get latest block")
    table.add_row("[bold green][2][/bold green]", "Get block by number")
    table.add_row("[bold green][3][/bold green]", "Get transaction by hash")
    table.add_row("[bold green][0][/bold green]", "Back")
    console.print(table)

    choice = Prompt.ask("Select", choices=["0", "1", "2", "3"], default="0")

    if choice == "1":
        block = explorer.get_latest_block()
        if block:
            explorer.print_block(block)
    elif choice == "2":
        num = Prompt.ask("Block number")
        block = explorer.get_block_by_number(int(num))
        if block:
            explorer.print_block(block)
    elif choice == "3":
        tx_hash = Prompt.ask("Transaction hash")
        tx = explorer.get_transaction(tx_hash)
        if tx:
            explorer.print_transaction(tx)

    input("\nPress Enter to return...")


def show_about() -> None:
    clear_screen()
    print_logo()

    about_path = BASE_DIR / "about.txt"
    about_text = "Monad BFT Network Toolkit"
    if about_path.exists():
        about_text = about_path.read_text(encoding="utf-8").strip()

    console.print(
        Panel(
            f"[bold cyan]About[/bold cyan]\n\n"
            f"{about_text}\n\n"
            "[dim]Monad is a high-performance Layer 1 blockchain with\n"
            "pipelined BFT consensus and parallel EVM execution.\n"
            "This toolkit provides monitoring, transaction building,\n"
            "and block exploration capabilities.[/dim]",
            border_style="magenta",
        )
    )
    input("\nPress Enter to return...")


@ensure_env
def main() -> None:
    while True:
        clear_screen()
        print_logo()

        console.print(
            Panel(
                "[bold green]Monad BFT Toolkit[/bold green]\n"
                "High-performance L1 network monitoring and interaction tools",
                border_style="green",
            )
        )

        table = Table(show_header=False, box=box.MINIMAL_DOUBLE_HEAD, padding=(0, 1))
        table.add_row("[bold green][1][/bold green]", "Install dependencies")
        table.add_row("[bold green][2][/bold green]", "Configure settings")
        table.add_row("[bold green][3][/bold green]", "Run node monitor")
        table.add_row("[bold green][4][/bold green]", "Transaction tools")
        table.add_row("[bold green][5][/bold green]", "Block explorer")
        table.add_row("[bold green][6][/bold green]", "About")
        table.add_row("[bold green][0][/bold green]", "Exit")
        console.print(table)

        choice = Prompt.ask(
            "\n[bold yellow]Select an option[/bold yellow]",
            choices=["0", "1", "2", "3", "4", "5", "6"],
            default="0",
        )

        if choice == "1":
            run_pip_install()
        elif choice == "2":
            configure_settings()
        elif choice == "3":
            run_node_monitor()
        elif choice == "4":
            transaction_tools()
        elif choice == "5":
            block_explorer()
        elif choice == "6":
            show_about()
        elif choice == "0":
            clear_screen()
            console.print("[bold green]Goodbye![/bold green]")
            return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupted.[/bold red]")
