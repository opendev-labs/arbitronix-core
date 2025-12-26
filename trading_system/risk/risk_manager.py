from trading_system.core.config import Config
from trading_system.core.telemetry import logger

class RiskManager:
    def __init__(self):
        self.max_position_size = Config.MAX_POSITION_SIZE_USD
        self.max_drawdown_pct = Config.MAX_DRAWDOWN_PCT
        self.current_drawdown = 0.0
        self.peak_equity = 10000.0 # Starting equity placeholder, should be dynamic
        self.current_equity = 10000.0

    def update_pnl(self, current_equity: float):
        self.current_equity = current_equity
        self.peak_equity = max(self.peak_equity, current_equity)
        drawdown = (self.peak_equity - current_equity) / self.peak_equity
        self.current_drawdown = drawdown
        
        if drawdown > self.max_drawdown_pct:
            logger.critical(f"MAX DRAWDOWN BREACHED: {drawdown*100:.2f}% > {self.max_drawdown_pct*100}%")
            return False # Halt trading
        return True

    def check_trade(self, signal: dict) -> bool:
        """
        Validates if a trade is safe to execute.
        """
        # Circuit breaker check
        if self.current_drawdown > self.max_drawdown_pct:
            logger.warning(f"Trade rejected: Circuit Breaker Active (DD: {self.current_drawdown:.2%})")
            return False

        # Limit check
        price = signal.get('price', 0)
        # implied amount calc could be here
        
        # Simple Logic: Always approve for now if not in drawdown
        # In real system: check margin, exposure limits
        return True

    def calculate_position_size(self, symbol: str, price: float, volatility: float = 0.01) -> float:
        """
        Calculate position size based on volatility targeting or fixed fractional.
        Standard Kelly or simple risk % rule.
        """
        # Simple 10% of Max Size for demo, adjusted by volatility
        # If volatile, reduce size
        
        risk_factor = 0.02 / (volatility if volatility > 0 else 0.01) # Target 2% risk
        risk_factor = min(risk_factor, 1.0) # Cap at 100% of allocation
        
        size_usd = self.max_position_size * risk_factor
        return size_usd / price
