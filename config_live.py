# Name of the file (without .py extension!) that contains the bot
bot_name = 'bots.bot_template'

# Datasource is poloniex or binance
datasource = 'binance'

revenyou_api_url = 'https://youhexpaper.revenyou.io/api/signal/v1/signal'

# Data settings real time data poloniex
data_settings_poloniex = {
    'max_length_ticker_data_list': 10, # the bot function receives a maximum of 10 ticker data at a time (the most recent ones)
    'id_pair_dictionary': { '148': 'BTC_ETH', '50': 'BTC_LTC' } # currency ids of BTC_ETH and BTC_LTC, see https://docs.poloniex.com/?shell#currencies
}

# Data settings real time data binance
data_settings_binance = {
    'max_length_ticker_data_list': 10, # the bot function receives a maximum of 10 ticker data at a time (the most recent ones)
    'pair_list': ['ethbtc', 'ltcbtc']  # Use ETH and LTC pricing data on the BTC market
}

buy_signal_settings = {
    'signal_provider': '[BOT NAME]',
    'signal_provider_key': '[KEY]',
    'exchange': datasource,
    'ethbtc': {
        'price_limit': '100', # Buy BTC with a price limit of 100 ETH
        'buy_ttl_sec': 1800, # Time (in seconds) for buy order to live
        'take_profit_price_percentage_60': '5', # Take 60% profit when price of BTC goes up with 5%
        'take_profit_price_percentage_40': '10', # Take 40% profit when price of BTC goes up with 10%
        'stop_loss_price_percentage': '5', # Close position (stop loss) when price of BTC  goes down with 5%
        'panic_sell_price_percentage': '20',
        "panic_sell_price_deviation_percentage": '2'
    },
    'ltcbtc': {
        'price_limit': '50', # Buy BTC with a price limit of 100 ETH
        'buy_ttl_sec': 1800, # Time (in seconds) for buy order to live
        'take_profit_price_percentage_60': '10', # Take 60% profit when price of BTC goes up with 5%
        'take_profit_price_percentage_40': '15', # Take 40% profit when price of BTC goes up with 10%
        'stop_loss_price_percentage': '10', # Close position (stop loss) when price of BTC  goes down with 5%
        'panic_sell_price_percentage': '15',
        "panic_sell_price_deviation_percentage": '3'
    }
}
