# market_analysis/implied_volatility_analyzer.py

import numpy as np
from scipy.stats import norm
from utils.black_scholes import black_scholes  # Assume you have Black-Scholes implementation

class ImpliedVolatilityAnalyzer:
    def __init__(self):
        self.risk_free_rate = 0.05  # Adjust based on current rates

    def calculate_iv(self, option_price, spot_price, strike_price, time_to_expiry, option_type='call'):
        """
        Calculate Implied Volatility using Black-Scholes model.
        """
        # Implement IV calculation using numerical methods (Newton-Raphson)
        # This is a simplified version - in practice, use a more robust method
        iv = 0.20  # Initial guess
        for _ in range(50):  # 50 iterations max
            bs_price = black_scholes(spot_price, strike_price, time_to_expiry, iv, self.risk_free_rate, option_type)
            vega = self.calculate_vega(spot_price, strike_price, time_to_expiry, iv, self.risk_free_rate)
            if vega == 0:
                break
            iv = iv - (bs_price - option_price) / vega
            if abs(bs_price - option_price) < 0.01:
                break
        return iv

    def calculate_vega(self, spot_price, strike_price, time_to_expiry, iv, risk_free_rate):
        """
        Calculate vega for Black-Scholes model.
        """
        d1 = (np.log(spot_price / strike_price) + (risk_free_rate + 0.5 * iv ** 2) * time_to_expiry) / (iv * np.sqrt(time_to_expiry))
        vega = spot_price * norm.pdf(d1) * np.sqrt(time_to_expiry)
        return vega

    def analyze_iv_rank(self, current_iv, historical_iv):
        """
        Calculate IV Rank (percentile of current IV vs historical IV).
        """
        iv_rank = (current_iv - min(historical_iv)) / (max(historical_iv) - min(historical_iv)) * 100
        return iv_rank

    def analyze_iv_percentile(self, current_iv, historical_iv):
        """
        Calculate IV Percentile (percentage of days when IV was lower than current).
        """
        iv_percentile = (sum(1 for iv in historical_iv if iv < current_iv) / len(historical_iv)) * 100
        return iv_percentile

# Example usage:
if __name__ == "__main__":
    iv_analyzer = ImpliedVolatilityAnalyzer()
    
    # Calculate IV for an option
    iv = iv_analyzer.calculate_iv(
        option_price=150, 
        spot_price=2500, 
        strike_price=2550, 
        time_to_expiry=0.1,  # ~36 days
        option_type='call'
    )
    print("Implied Volatility:", iv)