import pandas as pd
import numpy as np
from .base import BaseStrategy
from trading_system.core.telemetry import logger

class MeanReversionStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("mean_reversion_pro")
        self.zscore_entry = 2.0
        self.zscore_exit = 0.5
        self.min_periods = 20

    def calculate_hurst(self, price_series):
        """Calculate Hurst Exponent to determine mean-reverting nature"""
        try:
            lags = range(2, 20)
            tau = [np.sqrt(np.std(np.subtract(price_series[lag:], price_series[:-lag]))) for lag in lags]
            poly = np.polyfit(np.log(lags), np.log(tau), 1)
            return poly[0] * 2.0
        except:
            return 0.5

    def analyze(self, symbol, prices):
        if len(prices) < self.min_periods:
            return {'action': 'hold', 'reason': 'not enough data'}

        # Calculate Z-Score
        rolling_mean = prices.rolling(window=self.min_periods).mean()
        rolling_std = prices.rolling(window=self.min_periods).std()
        zscore = (prices - rolling_mean) / rolling_std
        
        current_z = zscore.iloc[-1]
        
        # Calculate Hurst Exponent (0-0.5 is mean reverting, 0.5-1 is trending)
        hurst = self.calculate_hurst(prices.values[-100:]) # Use last 100 candles for hurst
        
        signal = {
            'symbol': symbol,
            'zscore': current_z,
            'hurst': hurst,
            'price': prices.iloc[-1]
        }

        # Filter: Only trade mean reversion if Hurst < 0.6 (allowing slight noise)
        if hurst > 0.6:
            signal['action'] = 'hold'
            signal['reason'] = f'trending regime (H={hurst:.2f})'
            return signal

        if current_z < -self.zscore_entry:
            signal['action'] = 'buy'
            signal['side'] = 'long'
            signal['reason'] = f'oversold (z={current_z:.2f})'
        elif current_z > self.zscore_entry:
            signal['action'] = 'sell'
            signal['side'] = 'short'
            signal['reason'] = f'overbought (z={current_z:.2f})'
        else:
            signal['action'] = 'hold'
            signal['reason'] = f'within bounds (z={current_z:.2f})'
            
        return signal
