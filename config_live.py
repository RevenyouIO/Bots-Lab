# datasurce is poloniex or cryptocompare
datasource = 'poloniex'
revenYouApiUrl = 'https://signal.revenyou.io/api/signal/v1/signal'

# Data settings real time data poloniex
data_settings_poloniex = {
    'pair': 'ETH_BTC',  # Use ETH pricing data on the BTC market, ['ETH', 'BTC'] when datasource is cryptocompare
    'period': 1800,       # Use 1800 second candles
    'days_history': 100,  # Collect 100 days data
    'data_source': 'poloniex', # Datasource is polioniex or cryptocompare
}

# Data settings real time data cryptocompare
data_settings_cryptocompare = {
    'pair': ['ETH', 'BTC'],  # Use ETH pricing data on the BTC market, ['ETH', 'BTC'] when datasource is cryptocompare
    'days_history': 100,  # Collect 100 days data
    'exchange': 'Bitfinex' # exchange used when datasource is Cryptocompare
}

buy_signal_settings = {
    'signalProvider': '[NAME OF BOT]',
    'signalProviderKey': '[CODE]',
    'exchange': 'poloniex',
    'symbol': 'ETHBTC',
}
