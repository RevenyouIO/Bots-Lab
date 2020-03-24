# Name of the file (without .py extension!) that contains the bot
bot_name = 'rsi'

# Datasource is poloniex or cryptocompare
datasource = 'poloniex'

revenyou_api_url = 'https://youhex.revenyou.io/api/signal/v1/signal'

# Data settings real time data poloniex
data_settings_poloniex = {
    'pair': 'ETH_BTC',  # Use ETH pricing data on the BTC market
    'period': 1800,       # Use 1800 second candles
    'days_history': 10,  # Collect 10 days data
}

# Data settings real time data cryptocompare
data_settings_cryptocompare = {
    'pair': ['ETH', 'BTC'],  # Use ETH pricing data on the BTC market
    'days_history': 100,  # Collect 100 days data
    'exchange': 'Bitfinex' # Exchange that is used
}

buy_signal_settings = {
    'signal_provider': 'RsiBot',
    'signal_provider_key': 'Klp6LidLIE1',
    'exchange': datasource,
    'symbol': 'ETHBTC', # must be in line with the data settings object pair value!  
}
