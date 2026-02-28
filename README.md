# Monad-BFT
Monad BFT Toolkit — Network monitoring, transaction building, and block exploration tools for the Monad high-performance Layer 1 blockchain with pipelined BFT consensus and parallel EVM execution
<div align="center">

# Monad BFT Toolkit

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Monad](https://img.shields.io/badge/Monad-L1_EVM-00D4AA?style=for-the-badge)](https://monad.xyz)

**Network monitoring, transaction building, and block exploration toolkit for the Monad high-performance L1 blockchain.**

[Features](#features) · [Getting Started](#getting-started) · [Configuration](#configuration) · [Architecture](#architecture)

</div>

---

## Overview

Monad is a high-performance EVM-compatible Layer 1 blockchain featuring pipelined BFT consensus and parallel transaction execution. It targets 10,000+ TPS with sub-second finality while maintaining full Ethereum bytecode compatibility.

This toolkit provides Python-based utilities for interacting with Monad networks:

- **Node Monitor** — live dashboard tracking block height, gas prices, peer count, sync status, and throughput
- **Transaction Builder** — construct, sign, and broadcast native transfers and contract calls
- **Block Explorer** — query blocks, transactions, and receipts via JSON-RPC

---

## Features

| Feature | Description |
|---------|-------------|
| Live node dashboard | Real-time block height, gas price, peer count monitoring |
| Sync status tracking | Detect and display syncing progress |
| Throughput metrics | Blocks-per-second calculation over session lifetime |
| Native transfers | Build and sign ETH-equivalent transfers |
| Contract calls | Arbitrary calldata submission with gas estimation |
| Block inspection | Detailed block header and transaction listing |
| Transaction lookup | Query transaction details and receipts by hash |
| Gas estimation | Pre-flight gas estimation for any call |
| Rich TUI | Interactive terminal menu with styled output |
| Configurable | JSON-based config with interactive setup wizard |

---

## Getting Started

### Prerequisites

- Python 3.9+
- Access to a Monad JSON-RPC endpoint

### Installation

```bash
git clone https://github.com/example/monad-bft-toolkit.git
cd monad-bft-toolkit

pip install -r requirements.txt

python main.py
```

### Quick Setup

1. Run `python main.py` and select **Install dependencies**
2. Select **Configure settings** to set the RPC endpoint and chain ID
3. Use **Run node monitor** for a live dashboard
4. Use **Transaction tools** to build and send transactions
5. Use **Block explorer** to query on-chain data

---

## Configuration

Configuration is stored in `config.json`. Edit directly or use the interactive setup.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `rpc_url` | `https://testnet-rpc.monad.xyz` | Monad JSON-RPC endpoint |
| `chain_id` | `10143` | Network chain ID |
| `poll_interval` | `5` | Monitor refresh interval (seconds) |
| `block_history` | `20` | Blocks to display in explorer history |
| `gas_price_multiplier` | `1.1` | Multiplier for gas price bids |
| `timeout` | `30` | RPC request timeout (seconds) |

---

## Architecture

```
monad-bft-toolkit/
├── main.py              # TUI entry point (Rich-based menu)
├── monitor.py           # Live node monitor with Rich Live display
├── config.py            # Configuration load/save/interactive setup
├── tools/
│   ├── __init__.py      # Package init
│   ├── tx_builder.py    # Transaction construction and signing
│   └── explorer.py      # Block and transaction explorer via RPC
├── config.json          # Runtime configuration
├── requirements.txt     # Python dependencies
└── README.md
```

### Node Monitor

The monitor uses Rich `Live` rendering to display a continuously updating dashboard. It polls the RPC endpoint at the configured interval and tracks:

- Current block height and block production rate
- Gas price in both wei and Gwei
- Connected peer count
- Sync status (synced vs. syncing with progress)

### Transaction Builder

Supports two transaction types:

1. **Native transfers** — simple value transfers between addresses
2. **Contract calls** — arbitrary calldata with automatic gas estimation and configurable gas price multiplier

### Block Explorer

Provides read-only queries against the JSON-RPC endpoint:

- Latest block retrieval with full header details
- Block lookup by number
- Transaction lookup by hash with receipt information

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `rich` | Terminal UI, live display, tables, prompts |
| `requests` | HTTP client for JSON-RPC calls |
| `web3` | Ethereum/Monad interaction, transaction signing |
| `eth-account` | Private key management |

---

## Disclaimer

This toolkit is provided for **testnet and development purposes**. Always verify transaction parameters before signing. Never expose private keys in shared environments. The authors accept no responsibility for lost funds or misuse.

---

<div align="center">

**MIT License** · Contributions welcome

</div>
