# market_analysis/nifty_tools/option_chain_analyzer.py

import pandas as pd
import numpy as np
from utils.logger import logger

class NiftyOptionChainAnalyzer:
    def __init__(self):
        self.max_pain = None
        self.pcr = 0.0

    def fetch_option_chain(self, symbol='NIFTY', expiry='current'):
        """
        Fetch live option chain data from broker API.
        """
        # Implementation for fetching option chain
        # This would connect to your broker's API (Zerodha, Upstrobe, etc.)
        try:
            # Pseudocode for option chain data
            option_chain = {
                'strikes': [18000, 18100, 18200, 18300, 18400],
                'call_oi': [1200, 1500, 1800, 2100, 2400],
                'put_oi': [1800, 2100, 2400, 2700, 3000],
                'call_iv': [0.18, 0.19, 0.20, 0.21, 0.22],
                'put_iv': [0.22, 0.21, 0.20, 0.19, 0.18]
            }
            return option_chain
        except Exception as e:
            logger.error(f"Error fetching option chain: {str(e)}")
            return None

    def calculate_max_pain(self, option_chain):
        """
        Calculate Max Pain point for options.
        """
        strikes = option_chain['strikes']
        call_oi = option_chain['call_oi']
        put_oi = option_chain['put_oi']
        
        pain_points = []
        for strike in strikes:
            pain = sum([oi * max(0, strike - s) for s, oi in zip(strikes, call_oi)]) + \
                   sum([oi * max(0, s - strike) for s, oi in zip(strikes, put_oi)])
            pain_points.append(pain)
        
        self.max_pain = strikes[np.argmin(pain_points)]
        return self.max_pain

    def calculate_pcr(self, option_chain):
        """
        Calculate Put-Call Ratio.
        """
        total_put_oi = sum(option_chain['put_oi'])
        total_call_oi = sum(option_chain['call_oi'])
        
        self.pcr = total_put_oi / total_call_oi if total_call_oi > 0 else 0
        return self.pcr

    def analyze_iv_skew(self, option_chain):
        """
        Analyze volatility skew between calls and puts.
        """
        iv_skew = {}
        for strike, call_iv, put_iv in zip(option_chain['strikes'], 
                                         option_chain['call_iv'], 
                                         option_chain['put_iv']):
            iv_skew[strike] = {'call_iv': call_iv, 'put_iv': put_iv, 'skew': put_iv - call_iv}
        
        return iv_skew

# Example usage
if __name__ == "__main__":
    analyzer = NiftyOptionChainAnalyzer()
    option_chain = analyzer.fetch_option_chain()
    
    if option_chain:
        max_pain = analyzer.calculate_max_pain(option_chain)
        pcr = analyzer.calculate_pcr(option_chain)
        iv_skew = analyzer.analyze_iv_skew(option_chain)
        
        print(f"Max Pain: {max_pain}")
        print(f"PCR: {pcr:.2f}")
        print("IV Skew:", iv_skew)