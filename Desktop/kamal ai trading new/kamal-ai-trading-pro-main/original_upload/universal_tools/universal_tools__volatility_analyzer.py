# market_analysis/universal_tools/volatility_analyzer.py

class UniversalVolatilityAnalyzer:
    def __init__(self):
        self.volatility_thresholds = {
            'VERY_HIGH': 0.35,
            'HIGH': 0.25,
            'MODERATE': 0.18,
            'LOW': 0.12,
            'GENERIC': 0.20
        }
    
    def analyze_volatility_for_symbol(self, symbol, df):
        """
        Analyze volatility for any symbol with adaptive thresholds.
        """
        symbol_profile = get_symbol_profile(symbol)
        volatility_profile = symbol_profile['volatility_profile']
        
        # Calculate current volatility
        current_iv = self.calculate_current_iv(df)
        historical_iv = self.get_historical_iv(symbol)
        
        # Use appropriate threshold
        threshold = self.volatility_thresholds[volatility_profile]
        
        analysis = {
            'symbol': symbol,
            'current_iv': current_iv,
            'iv_percentile': self.calculate_iv_percentile(current_iv, historical_iv),
            'volatility_regime': self.get_volatility_regime(current_iv, threshold),
            'threshold_used': threshold
        }
        
        return analysis
    
    def get_volatility_regime(self, current_iv, threshold):
        """Determine volatility regime."""
        if current_iv > threshold * 1.3:
            return "VERY_HIGH_VOLATILITY"
        elif current_iv > threshold:
            return "HIGH_VOLATILITY"
        elif current_iv > threshold * 0.7:
            return "MODERATE_VOLATILITY"
        else:
            return "LOW_VOLATILITY"