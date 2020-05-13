import requests
import uuid
import importlib

from config_live import datasource, buy_signal_settings, revenyou_api_url, bot_name
from data.data_service import get_live_data_poloniex, get_live_data_cryptocompare, get_live_data_binance
from websocket_binance import BinanceWebsocketClient

def import_bot(name):
    try:
        return importlib.import_module(name)
    except ImportError:
        raise Exception(f'Bot module {name} does not exist')

def run_bot(data):
    bot = import_bot(name = bot_name)
    buy_or_sell_signal = bot.get_buy_or_sell_signal(data)
    # for now the revenyou api accepts only buy signals!
    if buy_or_sell_signal == 'buy':
        revenyou_api_signal = create_revenyou_buy_signal()
        request = requests.post(url = revenyou_api_url.strip("\n"), json = revenyou_api_signal, headers = {'content-type': 'application/json'})
        print(request.json())

def create_revenyou_buy_signal():
    api_signal = {    
        'signalProvider': buy_signal_settings.get('signal_provider'),
        'signalProviderKey': buy_signal_settings.get('signal_provider_key'),
        'exchange': buy_signal_settings.get('exchange'),
        'symbol': buy_signal_settings.get('symbol'),
        'signalType': 'buy',
        'signalId': str(uuid.uuid4()),
        'priceLimit': buy_signal_settings.get('price_limit'),
        'buyTTLSec': buy_signal_settings.get('buy_ttl_sec'),
        'takeProfit': [
            {
                'amountPercentage': '60',
                'pricePercentage': buy_signal_settings.get('take_profit_price_percentage_60')
            },
            {
                'amountPercentage': '40',
                'pricePercentage': buy_signal_settings.get('take_profit_price_percentage_40')
            }
        ],
        'stopLoss': {
            'pricePercentage': buy_signal_settings.get('stop_loss_price_percentage')
        },
        'panicSell': {
            'pricePercentage': buy_signal_settings.get('panic_sell_price_percentage'),
            'sellPriceDeviationPercentage': buy_signal_settings.get('panic_sell_price_deviation_percentage')
        }
    }

    return api_signal

def get_live_data():
    data = None
    if datasource == 'poloniex':
        data = get_live_data_poloniex()
    elif datasource == 'cryptocompare':
        data = get_live_data_cryptocompare()
    elif datasource == 'binance':
        data = get_live_data_binance()

    return data

# run periodically through cronjob
# live_data = get_live_data()
# run_bot(data = live_data)
ws = BinanceWebsocketClient()
ws.listen()
