# Name of the file (without .py extension!) that contains the bot
bot_name = 'bots.rsi'

# Example settings for backtesting engine
sim_params = {
    'capital_base': 10,      # Initial capital in BTC
    'fee': {
        'Long': 0.0015,      # Fee settings for Long
        'Short': 0.0015,     # Fee settings for Short
    },
    'resample': True, # For binance do not resample
    'data_frequency': '4H'  # Time frame to use (see /helpers/timeframe_resampler.py for more info)
}

# Datasource is poloniex, cryptocompare or binance
datasource = 'poloniex'

# Example data settings historical data poloniex (use the same base market for all pairs!)
# For more information: https://poloniex.com/
data_settings_list_poloniex = [ 
    {
        'pair': 'BTC_ETH',  # Use ETH pricing data on the BTC market
        'period': 1800,       # Use 1800 second candles
        'days_history': 100,  # Collect 100 days data
    },  
    {
        'pair': 'BTC_LTC',  # Use LTC pricing data on the BTC market
        'period': 1800,       # Use 1800 second candles
        'days_history': 100,  # Collect 100 days data
    }
]

# Example data settings historical data cryptocompare (use the same base market for all pairs!)
# For more information: https://www.cryptocompare.com/
data_settings_list_cryptocompare = [ 
    { 
        'pair': ['ETH', 'BTC'],  # Use ETH pricing data on the BTC market
        'days_history': 100,  # Collect 100 days data
        'exchange': 'Bitfinex' # exchange used when datasource is Cryptocompare
    },
    {
        'pair': ['LTC', 'BTC'],  # Use ETH pricing data on the BTC market
        'days_history': 100,  # Collect 100 days data
        'exchange': 'Bitfinex' # exchange used when datasource is Cryptocompare
    }
]

# Example data settings historical data binance (use the same base market for all pairs!)
# For more information: https://www.binance.com/
data_settings_list_binance = [
    {
        'pair': 'ETHBTC',  # Use ETH pricing data on the BTC market
        'period': '4h',   # Use 4 hour candles
        'limit': 100,  # Collect 100 candles
    },
    {
        'pair': 'LTCBTC',  # Use ETH pricing data on the BTC market
        'period': '4h',   # Use 4 hour candles
        'limit': 100,  # Collect 100 candles
    }
]
