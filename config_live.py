# Name of the file (without .py extension!) that contains the bot
bot_name = 'rsi'

# Datasource is poloniex or cryptocompare
datasource = 'poloniex'

revenyou_api_url = 'https://youhex.revenyou.io/api/signal/v1/signal'

# Data settings real time data poloniex
data_settings_poloniex = {
    'pair': 'BTC_ETH',  # Use ETH pricing data on the BTC market
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
    'signal_provider': '[NAME OF BOT]',
    'signal_provider_key': '[KEY]',
    'exchange': datasource,
    'symbol': 'BTCETH', # Must be in line with the data settings object pair value!  
    'price_limit': '100', # Buy BTC with a price limit of 100 ETH
    'buy_ttl_sec': 1800, # Time (in seconds) for buy order to live
    'take_profit_price_percentage': '10', # Take profit when price of BTC goes up with 10%
    'stop_loss_price_percentage': '5' # Close position (stop loss) when price of BTC  goes down with 5%
}
