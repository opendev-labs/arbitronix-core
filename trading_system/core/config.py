import os
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class TradingMode(Enum):
    PAPER = "PAPER"
    TESTNET = "TESTNET"
    LIVE = "LIVE"

class Config:
    # General
    TRADING_MODE = TradingMode(os.getenv("TRADING_MODE", "PAPER").upper())
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Binance Keys
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
    BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "")
    
    # Binance Testnet Keys
    BINANCE_TESTNET_API_KEY = os.getenv("BINANCE_TESTNET_API_KEY", "")
    BINANCE_TESTNET_SECRET_KEY = os.getenv("BINANCE_TESTNET_SECRET_KEY", "")

    # Symbols to trade
    SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
    
    # Risk Management
    MAX_POSITION_SIZE_USD = float(os.getenv("MAX_POSITION_SIZE_USD", "1000.0"))
    MAX_DRAWDOWN_PCT = float(os.getenv("MAX_DRAWDOWN_PCT", "0.05")) # 5% max drawdown
    
    # Paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"

    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    @classmethod
    def get_api_key(cls):
        if cls.TRADING_MODE == TradingMode.TESTNET:
            return cls.BINANCE_TESTNET_API_KEY
        return cls.BINANCE_API_KEY

    @classmethod
    def get_secret_key(cls):
        if cls.TRADING_MODE == TradingMode.TESTNET:
            return cls.BINANCE_TESTNET_SECRET_KEY
        return cls.BINANCE_SECRET_KEY

# Ensure directories exist
Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
