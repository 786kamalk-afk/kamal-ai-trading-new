# market_analysis/universal_tools/greek_calculator.py

class AdaptiveGreekCalculator:
    def calculate_greeks_for_symbol(self, symbol, spot_price, strike_price, 
                                  time_to_expiry, option_type='call'):
        """
        Calculate Greeks for any symbol with symbol-specific adjustments.
        """
        symbol_profile = get_symbol_profile(symbol)
        
        # Get appropriate risk-free rate and dividend yield
        risk_free_rate = self._get_risk_free_rate(symbol)
        dividend_yield = self._get_dividend_yield(symbol)
        
        # Calculate IV with symbol context
        iv = self._get_appropriate_iv(symbol, spot_price, strike_price)
        
        # Calculate all Greeks
        greeks = {
            'delta': self.calculate_delta(spot_price, strike_price, time_to_expiry, 
                                        iv, risk_free_rate, dividend_yield, option_type),
            'gamma': self.calculate_gamma(spot_price, strike_price, time_to_expiry, 
                                        iv, risk_free_rate, dividend_yield),
            'theta': self.calculate_theta(spot_price, strike_price, time_to_expiry, 
                                        iv, risk_free_rate, dividend_yield, option_type),
            'vega': self.calculate_vega(spot_price, strike_price, time_to_expiry, 
                                      iv, risk_free_rate, dividend_yield)
        }
        
        return greeks
    
    def _get_risk_free_rate(self, symbol):
        """Get appropriate risk-free rate for symbol."""
        # Different rates for different asset classes
        rates = {
            'NIFTY': 0.05,
            'BANKNIFTY': 0.05,
            'STOCKS': 0.06,
            'DEFAULT': 0.05
        }
        
        if symbol in rates:
            return rates[symbol]
        elif symbol in SYMBOL_PROFILES['INDICES']:
            return rates['NIFTY']
        else:
            return rates['STOCKS']