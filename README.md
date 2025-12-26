# ⚡ Arbitronix Core

> **Institutional-Grade Multi-Asset Trading Engine & Market Intelligence Suite**

Arbitronix Core is a high-performance, asynchronous trading framework designed for professional quant developers and startup-scale trading operations. Built with a "Reliability-First" philosophy, it handles real-time market data across multiple exchanges with integrated risk management and observability.

---

## 🚀 Key Features

- **Real-time Market Data Manager**: High-frequency Binance WebSocket integration with automatic reconnection and REST fallback logic.
- **Triple-Layer Strategy Engine**:
    - **Mean Reversion (Pro)**: Statistical Z-score logic with Hurst Exponent filtering to avoid "catching falling knives".
    - **Liquidity Sweep**: Detects market "fakeouts" and liquidity grabs using volume profiling.
    - **Hedged Pairs**: Co-integration based pair trading (e.g., BTC/ETH) with beta-neutral execution.
- **Institutional Risk Management**: Hard-coded circuit breakers, maximum drawdown limits, and volatility-adjusted position sizing.
- **3-Tier Execution Router**:
    - **Layer 1: Paper Trading** - Deterministic simulation for local testing.
    - **Layer 2: Testnet** - Live execution on Binance Testnet environment.
    - **Layer 3: Production** - High-concurrency execution with cryptographic key vaulting support.
- **Full Observability Suite**:
    - **Live Dashboard**: A premium, real-time Web UI for monitoring positions and PnL.
    - **Telegram Alerts**: Instant mobile notifications for all execution events.
    - **Audit Trail**: Detailed Loguru-powered telemetry with automated log rotation and compression.

---

## 🛠 Tech Stack

- **Core**: Python 3.11+, AsyncIO
- **Market Data**: Websockets / CCXT
- **Quantitative Engine**: NumPy, Pandas, TA-Lib
- **API/Dashboard**: FastAPI, Uvicorn, Vanilla CSS/JS
- **Infrastructure**: Docker, Docker Compose, Redis

---

## 📦 One-Click Deployment

Arbitronix is designed to be production-ready in 60 seconds.

```bash
# 1. Clone & Configure
cp .env.example .env
# Edit .env with your API keys

# 2. Deploy with Docker
docker-compose up --build -d
```

### Manual Setup
```bash
pip install -r requirements.txt
python main.py
```

---

## 📊 Dashboard

The system exposes a real-time monitoring interface at `http://localhost:8000`. It provides:
- Live aggregate equity tracking.
- Per-symbol Z-score and regime analytics.
- Visual signal indicators (BUY/SELL/HOLD).

---

## 🛡 Risk Disclosure

Trading cryptocurrencies involves significant risk. Arbitronix Core is provided "as is". Always test thoroughly on Testnet before deploying real capital.

---

## 📄 License & Attribution

Developed by **OpenDev Labs**. MIT License.
**Project Name**: Arbitronix Core
**Target Value**: $300M+ Startup Standard
