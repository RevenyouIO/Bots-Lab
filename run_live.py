import requests
from time import sleep
from config_live import datasource, buy_signal_settings, revenyou_api_url
from data.data_service import get_live_data_poloniex, get_live_data_cryptocompare
# choose here which bot function to import
from rsi import get_buy_or_sell_signal

def run_bot(data):
    buy_or_sell_signal = get_buy_or_sell_signal(data)
    if buy_or_sell_signal is not None:
        revenyou_api_signal = create_revenyou_api_signal(signal = buy_or_sell_signal)
        request = requests.post(url = revenyou_api_url, data = revenyou_api_signal, headers = {'Content-type': 'application/json'})
        print(request)

def create_revenyou_api_signal(signal):
    api_signal = {    
        "signalProvider": buy_signal_settings.get('signal_provider'),
        "signalProviderKey": buy_signal_settings.get('signal_provider_key'),
        "exchange": buy_signal_settings.get('exchange'),
        "symbol": buy_signal_settings.get('symbol'),
        "signalType": signal,
    }

    return api_signal

def get_live_data():
    data = None
    if datasource == 'poloniex':
        data = get_live_data_poloniex()
    elif datasource == 'cryptocompare':
        data = get_live_data_cryptocompare()

    return data

# run periodically through cronjob
live_data = get_live_data()
run_bot(data = live_data)
