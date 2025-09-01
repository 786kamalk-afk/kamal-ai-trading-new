# market_analysis/advanced_chart_analyzer.py

import pandas as pd
import numpy as np
import talib
from datetime import datetime
import logging
from utils.logger import logger
from data_ingestion.live_data_connectors import get_live_price, get_historical_data

class AdvancedChartAnalyzer:
    def __init__(self):
        self.patterns = []
        self.support_levels = []
        self.resistance_levels = []

    def identify_candlestick_patterns(self, df):
        """
        Recognize common candlestick patterns using TA-Lib.
        """
        patterns = {}
        pattern_names = [
            'CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3INSIDE', 'CDL3LINESTRIKE', 'CDL3OUTSIDE', 'CDL3STARSINSOUTH',
            'CDL3WHITESOLDIERS', 'CDLABANDONEDBABY', 'CDLADVANCEBLOCK', 'CDLBELTHOLD', 'CDLBREAKAWAY', 'CDLCLOSINGMARUBOZU',
            'CDLCONCEALBABYSWALL', 'CDLCOUNTERATTACK', 'CDLDARKCLOUDCOVER', 'CDLDOJI', 'CDLDOJISTAR', 'CDLDRAGONFLYDOJI',
            'CDLENGULFING', 'CDLEVENINGDOJISTAR', 'CDLEVENINGSTAR', 'CDLGAPSIDESIDEWHITE', 'CDLGRAVESTONEDOJI', 'CDLHAMMER',
            'CDLHANGINGMAN', 'CDLHARAMI', 'CDLHARAMICROSS', 'CDLHIGHWAVE', 'CDLHIKKAKE', 'CDLHIKKAKEMOD', 'CDLHOMINGPIGEON',
            'CDLIDENTICAL3CROWS', 'CDLINNECK', 'CDLINVERTEDHAMMER', 'CDLKICKING', 'CDLKICKINGBYLENGTH', 'CDLLADDERBOTTOM',
            'CDLLONGLEGGEDDOJI', 'CDLLONGLINE', 'CDLMARUBOZU', 'CDLMATCHINGLOW', 'CDLMATHOLD', 'CDLMORNINGDOJISTAR',
            'CDLMORNINGSTAR', 'CDLONNECK', 'CDLPIERCING', 'CDLRICKSHAWMAN', 'CDLRISEFALL3METHODS', 'CDLSEPARATINGLINES',
            'CDLSHOOTINGSTAR', 'CDLSHORTLINE', 'CDLSPINNINGTOP', 'CDLSTALLEDPATTERN', 'CDLSTICKSANDWICH', 'CDLTAKURI',
            'CDLTASUKIGAP', 'CDLTHRUSTING', 'CDLTRISTAR', 'CDLUNIQUE3RIVER', 'CDLUPSIDEGAP2CROWS', 'CDLXSIDEGAP3METHODS'
        ]

        for pattern in pattern_names:
            try:
                pattern_func = getattr(talib, pattern)
                result = pattern_func(df['open'], df['high'], df['low'], df['close'])
                last_result = result.iloc[-1]
                if last_result != 0:
                    patterns[pattern] = last_result
            except Exception as e:
                logger.error(f"Error detecting pattern {pattern}: {str(e)}")

        return patterns

    def calculate_support_resistance(self, df, window=20):
        """
        Calculate support and resistance levels using recent pivots.
        """
        df['pivot_low'] = df['low'].rolling(window=window, center=True).min()
        df['pivot_high'] = df['high'].rolling(window=window, center=True).max()

        support_levels = df['pivot_low'].dropna().unique().tolist()
        resistance_levels = df['pivot_high'].dropna().unique().tolist()

        return support_levels, resistance_levels

    def calculate_implied_volatility(self, option_chain):
        """
        Calculate Implied Volatility from option chain data.
        """
        iv_data = {}
        for strike, options in option_chain.items():
            if 'call' in options and 'put' in options:
                call_iv = options['call']['impliedVolatility']
                put_iv = options['put']['impliedVolatility']
                iv_data[strike] = {'call_iv': call_iv, 'put_iv': put_iv}

        return iv_data

    def analyze_volatility_skew(self, iv_data):
        """
        Analyze volatility skew between calls and puts.
        """
        skew = {}
        for strike, ivs in iv_data.items():
            skew[strike] = ivs['call_iv'] - ivs['put_iv']

        return skew

    def generate_chart_based_signals(self, symbol, timeframe='15min'):
        """
        Generate trading signals based on chart analysis.
        """
        df = get_historical_data(symbol, timeframe=timeframe, limit=100)
        if df is None or df.empty:
            return None

        signals = []

        # 1. Candlestick Patterns
        patterns = self.identify_candlestick_patterns(df)
        if patterns:
            signals.append({'type': 'candlestick_pattern', 'data': patterns})

        # 2. Support/Resistance
        support, resistance = self.calculate_support_resistance(df)
        signals.append({'type': 'support', 'levels': support})
        signals.append({'type': 'resistance', 'levels': resistance})

        # 3. Trend Analysis (using EMA)
        df['ema_20'] = talib.EMA(df['close'], timeperiod=20)
        df['ema_50'] = talib.EMA(df['close'], timeperiod=50)
        current_ema20 = df['ema_20'].iloc[-1]
        current_ema50 = df['ema_50'].iloc[-1]

        if current_ema20 > current_ema50:
            signals.append({'type': 'trend', 'direction': 'bullish'})
        else:
            signals.append({'type': 'trend', 'direction': 'bearish'})

        return signals

# Example usage:
if __name__ == "__main__":
    chart_analyzer = AdvancedChartAnalyzer()
    
    # Analyze chart for a symbol
    signals = chart_analyzer.generate_chart_based_signals('RELIANCE')
    print("Chart Signals:", signals)
    
    # Analyze IV for options
    option_chain = get_option_chain('RELIANCE')  # Assume this function exists
    iv_data = chart_analyzer.calculate_implied_volatility(option_chain)
    skew = chart_analyzer.analyze_volatility_skew(iv_data)
    print("IV Skew:", skew)