# market_analysis/nifty_tools/greek_calculator.py

from scipy.stats import norm

class GreekCalculator:
    def __init__(self, risk_free_rate=0.05):
        self.risk_free_rate = risk_free_rate

    def calculate_delta(self, spot, strike, time_to_expiry, iv, option_type='call'):
        """
        Calculate Delta for options.
        """
        d1 = (np.log(spot/strike) + (self.risk_free_rate + 0.5*iv**2)*time_to_expiry) / (iv*np.sqrt(time_to_expiry))
        if option_type == 'call':
            return norm.cdf(d1)
        else:
            return norm.cdf(d1) - 1

    def calculate_gamma(self, spot, strike, time_to_expiry, iv):
        """
        Calculate Gamma for options.
        """
        d1 = (np.log(spot/strike) + (self.risk_free_rate + 0.5*iv**2)*time_to_expiry) / (iv*np.sqrt(time_to_expiry))
        return norm.pdf(d1) / (spot * iv * np.sqrt(time_to_expiry))

    def calculate_theta(self, spot, strike, time_to_expiry, iv, option_type='call'):
        """
        Calculate Theta for options.
        """
        d1 = (np.log(spot/strike) + (self.risk_free_rate + 0.5*iv**2)*time_to_expiry) / (iv*np.sqrt(time_to_expiry))
        d2 = d1 - iv * np.sqrt(time_to_expiry)
        
        if option_type == 'call':
            theta = - (spot * norm.pdf(d1) * iv) / (2 * np.sqrt(time_to_expiry)) - \
                    self.risk_free_rate * strike * np.exp(-self.risk_free_rate*time_to_expiry) * norm.cdf(d2)
        else:
            theta = - (spot * norm.pdf(d1) * iv) / (2 * np.sqrt(time_to_expiry)) + \
                    self.risk_free_rate * strike * np.exp(-self.risk_free_rate*time_to_expiry) * norm.cdf(-d2)
        
        return theta / 365  # Daily theta

    def calculate_all_greeks(self, spot, strike, time_to_expiry, iv, option_type='call'):
        """
        Calculate all major Greeks.
        """
        return {
            'delta': self.calculate_delta(spot, strike, time_to_expiry, iv, option_type),
            'gamma': self.calculate_gamma(spot, strike, time_to_expiry, iv),
            'theta': self.calculate_theta(spot, strike, time_to_expiry, iv, option_type),
            'vega': self.calculate_vega(spot, strike, time_to_expiry, iv)
        }