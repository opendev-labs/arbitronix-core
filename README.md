# ⚡ Arbitronix Core
![Arbitronix Banner](https://raw.githubusercontent.com/opendev-labs/arbitronix-core-/main/docs/logo_placeholder.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/opendev-labs/arbitronix-core-/actions/workflows/main.yml/badge.svg)](https://github.com/opendev-labs/arbitronix-core-/actions/workflows/main.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![DeepMind Tech Stack](https://img.shields.io/badge/Tech--Stack-DeepMind--Level-purple.svg)](#)

> **Institutional-Grade Multi-Asset Trading Engine & Market Intelligence Suite**

Arbitronix Core is a high-performance, asynchronous trading framework designed for professional quant developers and startup-scale trading operations. Built with a "Reliable-First" philosophy, it handles real-time market data across multiple exchanges with integrated risk management and observability.

[**Explore Landing Page**](https://opendev-labs.github.io/arbitronix-core-) | [**Documentation**](#) | [**Report Bug**](https://github.com/opendev-labs/arbitronix-core-/issues)

---

## 🏛 Technical Architecture

The system is designed with a decoupled producer-consumer architecture, ensuring sub-millisecond latency between market events and execution signals.

```mermaid
graph TD
    A[Binance WS Manager] -->|Real-time Feed| B(Core Data Buffer)
    B --> C{Strategy Router}
    C -->|Mean Reversion| D[MR Strategy Pro]
    C -->|Liquidity Sweep| E[LS Strategy]
    C -->|Pair Trading| F[PT Strategy]
    D & E & F -->|Signal| G[Risk Manager]
    G -->|Valid Signal| H[Execution Adapter]
    H -->|Market/Limit| I[Exchanges]
    B --> J[FastAPI Dashboard]
    J -->|Live Stream| K((Web Console))
```

---

## 🚀 Enterprise Features

### 1. Quantum Market Data Manager
- **Resilient WebSockets**: Multi-channel Binance integration with automatic exponential backoff.
- **REST Fallback**: Zero-gap data integrity via secondary polling fallback.
- **Correlation Engine**: Real-time rolling cross-asset correlation matrix for portfolio hedging.

### 2. Advanced Quant Strategy Suite
- **Mean Reversion Pro**: Statistical Z-Score logic enhanced with **Hurst Exponent** regime detection (Avoids trading in trending markets).
- **Liquidity Sweep Manager**: Detects institutional liquidity grabs at historical extremes using volume profiling.
- **Hedged Pairs**: Statistical co-integration arbitrage between asset pairs (e.g., BTC-ETH spread).

### 3. Institutional Risk Guard
- **Circuit Breakers**: Global Maximum Drawdown and Volatility spikes protection.
- **Sizing Logic**: Dynamic position sizing based on Kelly Criterion and Volatility Scaling.
- **Safety Filters**: Automatic position closure on market regime shifts.

---

## 🛠 Tech Stack & Engineering

- **Infrastructure**: Docker Orchestration, multi-stage builds.
- **Runtime**: Python 3.11+, AsyncIO / uvloop.
- **Storage/Cache**: Redis for state persistence.
- **Quantitative**: NumPy, Pandas, CCXT.
- **Observability**: FastAPI, Loguru Structured Logging, CSS3 Glassmorphism UI.

---

## 📦 One-Click Deployment

```bash
# 1. Clone the Institutional Repository
git clone https://github.com/opendev-labs/arbitronix-core-.git
cd arbitronix-core-

# 2. Automated Environment Setup
./scripts/setup.sh

# 3. Deploy
docker-compose up --build -d
```

---

## 📊 Missions Control UI

The system serves a high-fidelity monitoring console at `http://localhost:8000`.
- **Live Visuals**: Real-time Z-score heatmaps and execution logs.
- **Command Deck**: Toggle strategies and risk parameters on-the-fly.
- **Global PnL**: Real-time unrealized PnL tracking across all sub-accounts.

---

## 🛡 Security & Compliance

- **Key Vaulting**: Sensitive API credentials are never logged and are managed via `.env` injection.
- **Audit Trails**: cryptographically verifiable event logs for institutional compliance.
- **Security Policy**: See [SECURITY.md](SECURITY.md) for vulnerability reporting.

---

## 📄 License & Ownership

Developed & Maintained by **OpenDev Labs**.
Licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

*"Building the future of decentralized institutional finance."*
