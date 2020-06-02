import importlib
import logging
logging.basicConfig(level=logging.DEBUG)

from config_live import datasource, bot_name
from data.websocket_binance import BinanceWebsocketClient
from data.websocket_poloniex import PoloniexWebsocketClient

def import_bot(name):
    try:
        return importlib.import_module(name)
    except ImportError:
        raise Exception(f'Bot module {name} does not exist')

bot = import_bot(name=bot_name)
if datasource == 'binance':
    ws = BinanceWebsocketClient(get_buy_or_sell_signal=bot.get_buy_or_sell_signal)
    ws.listen()
elif datasource == 'poloniex':
    ws = PoloniexWebsocketClient(get_buy_or_sell_signal=bot.get_buy_or_sell_signal)
    ws.listen()
        
        
