# market_analysis/nifty_tools/volatility_analyzer.py

import numpy as np
import pandas as pd

class NiftyVolatilityAnalyzer:
    def __init__(self):
        self.historical_vol = 0.0
        self.implied_vol = 0.0
        self.volatility_ratio = 0.0

    def calculate_historical_volatility(self, df, period=20):
        """
        Calculate historical volatility.
        """
        returns = np.log(df['close'] / df['close'].shift(1))
        self.historical_vol = returns.std() * np.sqrt(252)  # Annualized
        return self.historical_vol

    def analyze_volatility_regime(self, current_iv, historical_iv):
        """
        Identify volatility regime.
        """
        iv_percentile = np.percentile(historical_iv, current_iv)
        
        if iv_percentile > 70:
            return "HIGH_VOLATILITY"
        elif iv_percentile < 30:
            return "LOW_VOLATILITY"
        else:
            return "MODERATE_VOLATILITY"

    def generate_volatility_signals(self, symbol='NIFTY'):
        """
        Generate trading signals based on volatility analysis.
        """
        # Fetch data
        df = get_historical_data(symbol, timeframe='1d', limit=100)
        option_chain = get_option_chain(symbol)
        
        # Calculate volatilities
        hist_vol = self.calculate_historical_volatility(df)
        impl_vol = np.mean([option_chain['call_iv'] + option_chain['put_iv']]) / 2
        
        # Volatility ratio
        self.volatility_ratio = impl_vol / hist_vol
        
        signals = []
        if self.volatility_ratio > 1.2:
            signals.append({'type': 'VOL_EXPANSION', 'action': 'SELL_VOLATILITY'})
        elif self.volatility_ratio < 0.8:
            signals.append({'type': 'VOL_COMPRESSION', 'action': 'BUY_VOLATILITY'})
        
        return signals