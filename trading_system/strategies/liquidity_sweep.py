import pandas as pd
import numpy as np
from .base import BaseStrategy

class LiquiditySweepStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("liquidity_sweep")
        self.lookback_period = 50
    
    def analyze(self, symbol, prices):
        # We need High/Low data for sweeps, usually purely close price isn't enough.
        # Assuming prices is a Series of Closes, we can't do true sweep detection.
        # But if the system passed High/Low, we could.
        # For compatibility with simple `analyze(symbol, prices)` interface which passes Series,
        # we will use local swing high/lows on Close prices as proxy.
        
        if len(prices) < self.lookback_period:
            return {'action': 'hold', 'reason': 'not enough data'}
            
        # Detect Swing High/Low
        # recent_high = prices.iloc[-self.lookback_period:-5].max() 
        # We look for a price that breaks the recent high but closes below it (Bearish Sweep)
        # or breaks low and closes above (Bullish Sweep).
        
        # Since we only receive 'prices' (likely closes), we can simulate a "sweep"
        # by checking if CURRENT price is reversing violently from a recent extreme.
        
        recent_window = prices.iloc[-self.lookback_period:]
        recent_high = recent_window.max()
        recent_low = recent_window.min()
        
        current_price = prices.iloc[-1]
        prev_price = prices.iloc[-2]
        
        # Simple Fakeout logic on Close
        # If we were at high, and now rejecting fast
        
        signal = {'symbol': symbol, 'price': current_price, 'action': 'hold', 'reason': 'no sweep'}
        
        # Mock logic for "Sweep" without full OHLC
        # If price was very close to high (>98% range) and now drops
        range_high = recent_high
        range_low = recent_low
        
        if (prev_price >= range_high * 0.999) and (current_price < prev_price * 0.995):
            signal['action'] = 'sell'
            signal['side'] = 'short'
            signal['reason'] = 'liquidity sweep high'
            
        elif (prev_price <= range_low * 1.001) and (current_price > prev_price * 1.005):
            signal['action'] = 'buy'
            signal['side'] = 'long'
            signal['reason'] = 'liquidity sweep low'
            
        return signal
