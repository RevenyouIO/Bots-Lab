import importlib
from time import sleep

from config_live import datasource, bot_name, data_settings_cryptocompare, data_settings_poloniex
from data.data_service import get_live_data_poloniex, get_live_data_cryptocompare
from websocket_binance import BinanceWebsocketClient
from api_service import send_request

def import_bot(name):
    try:
        return importlib.import_module(name)
    except ImportError:
        raise Exception(f'Bot module {name} does not exist')

def run_bot(time_interval, get_buy_or_sell_signal):
    while True:
        live_data = get_live_data()
        buy_or_sell_signal = get_buy_or_sell_signal(live_data)
        # for now the revenyou api accepts only buy signals!
        print(buy_or_sell_signal)
        if buy_or_sell_signal == 'buy':
            send_request()
        sleep(time_interval)

def get_live_data():
    data = None
    if datasource == 'poloniex':
        data = get_live_data_poloniex()
    elif datasource == 'cryptocompare':
        data = get_live_data_cryptocompare()

    return data

bot = import_bot(name=bot_name)
if datasource == 'binance':
    ws = BinanceWebsocketClient(get_buy_or_sell_signal=bot.get_buy_or_sell_signal)
    ws.listen()
else:
    time_interval = 1800
    if datasource == 'poloniex':
        time_interval = data_settings_poloniex.get('bot_function_interval')
    elif datasource == 'cryptocompare':
        time_interval = data_settings_cryptocompare.get('bot_function_interval')
        
    run_bot(time_interval=time_interval, get_buy_or_sell_signal=bot.get_buy_or_sell_signal)
        
        
