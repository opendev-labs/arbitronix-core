import pandas as pd
import numpy as np

class Analytics:
    def calculate_zscore(self, series, window=20):
        rolling_mean = series.rolling(window=window).mean()
        rolling_std = series.rolling(window=window).std()
        return (series - rolling_mean) / rolling_std
    
    def detect_regime(self, prices):
        returns = prices.pct_change().dropna()
        volatility = returns.std()
        if volatility > returns.std() * 1.5:
            return "volatile"
        elif abs(prices.diff().mean()) / prices.mean() > 0.001:
            return "trending"
        return "ranging"
