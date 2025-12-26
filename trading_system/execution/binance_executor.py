import ccxt
import time
from typing import Dict, Any
from trading_system.core.config import Config
from trading_system.core.telemetry import logger

class BinanceExecutor:
    def __init__(self):
        self.mode = Config.TRADING_MODE
        self.api_key = Config.get_api_key()
        self.secret_key = Config.get_secret_key()
        
        self.client = None
        if self.mode in [Config.TRADING_MODE.TESTNET, Config.TRADING_MODE.LIVE]:
            self._init_client()

    def _init_client(self):
        try:
            self.client = ccxt.binance({
                'apiKey': self.api_key,
                'secret': self.secret_key,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future'  # Assuming Futures trading for hedging
                }
            })
            if self.mode == Config.TRADING_MODE.TESTNET:
                self.client.set_sandbox_mode(True)
            
            logger.info(f"Initialized Binance Executor in {self.mode.value} mode")
        except Exception as e:
            logger.critical(f"Failed to initialize Binance Client: {e}")

    def execute_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute order on Binance.
        Order dict expected: {'symbol': 'BTC/USDT', 'side': 'buy', 'amount': 0.001, 'type': 'market'}
        """
        if self.mode == Config.TRADING_MODE.PAPER:
            logger.info(f"PAPER EXECUTION: {order}")
            return {"status": "filled", "id": f"paper_{int(time.time())}", "info": order}

        if not self.client:
            logger.error("Client not initialized for Live/Testnet execution")
            return {"status": "failed", "reason": "client_not_ready"}

        try:
            symbol = order['symbol'].replace("USDT", "/USDT") # CCXT format
            side = order['side']
            amount = order.get('amount')
            order_type = order.get('type', 'market')
            
            logger.info(f"Sending Order to Binance: {side} {amount} {symbol} ({order_type})")
            
            if order_type == 'market':
                response = self.client.create_market_order(symbol, side, amount)
            else:
                price = order.get('price')
                response = self.client.create_limit_order(symbol, side, amount, price)
                
            logger.success(f"Order Executed: {response['id']}")
            return response
            
        except Exception as e:
            logger.error(f"Order Execution Failed: {e}")
            return {"status": "failed", "reason": str(e)}

    def get_positions(self):
        if self.mode == Config.TRADING_MODE.PAPER:
            return []
        try:
            # Fetch futures positions
            balance = self.client.fetch_balance()
            positions = [p for p in balance['info']['positions'] if float(p['positionAmt']) != 0]
            return positions
        except Exception as e:
            logger.error(f"Failed to fetch positions: {e}")
            return []
