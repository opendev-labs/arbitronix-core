import pandas as pd
import numpy as np
from datetime import datetime

class DataFetcher:
    def __init__(self):
        self.data_cache = {}
    
    def get_mock_data(self, symbol, periods=100):
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='15min')
        prices = np.cumprod(1 + np.random.randn(periods) * 0.001) * 50000
        data = pd.DataFrame({
            'timestamp': dates,
            'open': prices * 0.999,
            'high': prices * 1.002,
            'low': prices * 0.998,
            'close': prices,
            'volume': np.random.rand(periods) * 1000
        })
        self.data_cache[symbol] = data
        return data
