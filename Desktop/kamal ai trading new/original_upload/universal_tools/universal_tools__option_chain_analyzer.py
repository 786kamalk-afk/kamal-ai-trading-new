# market_analysis/universal_tools/option_chain_analyzer.py

class UniversalOptionChainAnalyzer:
    def __init__(self):
        self.supported_symbols = {
            'INDICES': ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'SENSEX'],
            'STOCKS': ['RELIANCE', 'HDFCBANK', 'INFY', 'TCS', 'ICICIBANK'],
            'SECTORS': ['AUTO', 'BANK', 'IT', 'FMCG', 'METAL']
        }
    
    def analyze_any_symbol(self, symbol, expiry='current'):
        """
        Analyze option chain for ANY supported symbol.
        """
        if symbol not in self._get_all_supported_symbols():
            logger.warning(f"Symbol {symbol} not in supported list. Extending analysis...")
            # Automatically extend to new symbols
            self.supported_symbols['CUSTOM'].append(symbol)
        
        return self._fetch_and_analyze_chain(symbol, expiry)
    
    def _get_all_supported_symbols(self):
        """Get all supported symbols across categories."""
        all_symbols = []
        for category, symbols in self.supported_symbols.items():
            all_symbols.extend(symbols)
        return all_symbols
    
    def _fetch_and_analyze_chain(self, symbol, expiry):
        """Universal option chain analysis logic."""
        # Common analysis logic that works for any symbol
        option_chain = self.fetch_option_chain(symbol, expiry)
        
        analysis_results = {
            'symbol': symbol,
            'max_pain': self.calculate_max_pain(option_chain),
            'pcr': self.calculate_pcr(option_chain),
            'iv_skew': self.analyze_iv_skew(option_chain),
            'top_strikes': self.get_high_oi_strikes(option_chain)
        }
        
        return analysis_results