import pandas as pd
import numpy as np
from typing import Dict, List
from trading_system.core.telemetry import logger

class CorrelationEngine:
    def __init__(self, symbols: List[str], window_size: int = 50):
        self.symbols = symbols
        self.window_size = window_size
        self.price_history: Dict[str, List[float]] = {s: [] for s in symbols}
        self.returns_df = pd.DataFrame()

    def update_price(self, symbol: str, price: float):
        if symbol not in self.price_history:
            return
            
        self.price_history[symbol].append(price)
        if len(self.price_history[symbol]) > self.window_size + 1:
             self.price_history[symbol].pop(0)

    def calculate_correlations(self) -> pd.DataFrame:
        # Construct DataFrame
        data = {}
        min_len = float('inf')
        
        for s in self.symbols:
            l = len(self.price_history[s])
            if l < 10: # Minimum data needed
                return pd.DataFrame()
            min_len = min(min_len, l)

        # Align lengths
        for s in self.symbols:
            data[s] = self.price_history[s][-min_len:]
            
        df = pd.DataFrame(data)
        
        # Calculate returns
        returns = df.pct_change().dropna()
        
        if returns.empty:
            return pd.DataFrame()
            
        # Correlation matrix
        corr_matrix = returns.corr()
        return corr_matrix

    def get_beta(self, target_symbol: str, benchmark_symbol: str) -> float:
        # Calculate beta: Cov(r_target, r_benchmark) / Var(r_benchmark)
        # Needs aligned data
        # Simply use the cached calculation logic or recompute
        # For efficiency, we reuse calculate_correlations logic if expanded
        # Here we do a quick ad-hoc for simplicity
        
        if len(self.price_history[target_symbol]) < 20 or len(self.price_history[benchmark_symbol]) < 20:
            return 1.0

        s1 = pd.Series(self.price_history[target_symbol])
        s2 = pd.Series(self.price_history[benchmark_symbol])
        
        # Truncate to match
        l = min(len(s1), len(s2))
        s1 = s1.iloc[-l:]
        s2 = s2.iloc[-l:]
        
        r1 = s1.pct_change().dropna()
        r2 = s2.pct_change().dropna()
        
        cov = r1.cov(r2)
        var = r2.var()
        
        if var == 0:
            return 1.0
            
        return cov / var
