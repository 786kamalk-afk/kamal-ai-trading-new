# market_analysis/nifty_tools/market_depth_analyzer.py

class MarketDepthAnalyzer:
    def __init__(self):
        self.bid_ask_spread = 0.0
        self.liquidity_zones = {}

    def analyze_market_depth(self, depth_data):
        """
        Analyze order book depth.
        """
        bids = depth_data['bids']
        asks = depth_data['asks']
        
        # Calculate bid-ask spread
        self.bid_ask_spread = asks[0]['price'] - bids[0]['price']
        
        # Identify liquidity zones
        self.liquidity_zones = {
            'support': self._find_liquidity_zone(bids),
            'resistance': self._find_liquidity_zone(asks)
        }
        
        return {
            'spread': self.bid_ask_spread,
            'liquidity_zones': self.liquidity_zones
        }

    def _find_liquidity_zone(self, orders):
        """
        Find price levels with significant liquidity.
        """
        total_quantity = sum(order['quantity'] for order in orders)
        liquidity_zones = []
        
        for order in orders:
            if order['quantity'] > total_quantity * 0.1:  # More than 10% of total
                liquidity_zones.append({
                    'price': order['price'],
                    'quantity': order['quantity']
                })
        
        return liquidity_zones