import requests
from time import sleep
from config_live import datasource, buy_signal_settings, revenYouApiUrl
from data.data_service import get_real_time_data_poloniex, get_real_time_data_cryptocompare
# choose here which logic function to import
from rsi import bot

def runBot(data):
    signal = bot(data)
    buy_signal = create_buy_signal(signal)
    request = requests.post(revenYouApiUrl, data = buy_signal, headers = {'Content-type': 'application/json'})
    print(request)

def create_buy_signal(signal):
    bs = {    
        "signalProvider": buy_signal_settings.get('signalProvider'),
        "signalProviderKey": buy_signal_settings.get('signalProviderKey'),
        "exchange": buy_signal_settings.get('exchange'),
        "symbol": buy_signal_settings.get('symbol'),
        "signalType": signal,
    }

    return bs

def getRealTimeData():
    data = None
    if datasource == 'poloniex':
        data = get_real_time_data_poloniex()
    elif datasource == 'cryptocompare':
        data = get_real_time_data_cryptocompare()

    return data

# run periodically by cronjob
realtime_data = getRealTimeData()
runBot(realtime_data)
