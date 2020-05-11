from data import poloniex as px
from data import cryptocompare as cc
from data import binance as bn
# from config_test import data_settings_poloniex, data_settings_cryptocompare, data_settings_binance
from config_live import data_settings_poloniex as dsp, data_settings_cryptocompare as dsc, data_settings_binance as dsb

def get_historical_data_poloniex(data_settings_poloniex):
    pair = data_settings_poloniex.get('pair')
    period = data_settings_poloniex.get('period')
    days_history = data_settings_poloniex.get('days_history')

    return px.load_dataframe(pair, period, days_history)

def get_historical_data_cryptocompare(data_settings_cryptocompare):
    pair = data_settings_cryptocompare.get('pair')
    days_history = data_settings_cryptocompare.get('days_history')
    exchange = data_settings_cryptocompare.get('exchange')

    return cc.load_dataframe(pair, days_history, exchange)

def get_historical_data_binance(data_settings_binance):
    pair = data_settings_binance.get('pair')
    period = data_settings_binance.get('period')
    limit = data_settings_binance.get('limit')

    return bn.load_dataframe(pair, period, limit)

def get_live_data_poloniex():
    pair = dsp.get('pair')
    period = dsp.get('period')
    days_history = dsp.get('days_history')

    # return live data from poloniex (historical and/or realtime)
    return px.load_dataframe(pair, period, days_history)

def get_live_data_cryptocompare():
    pair = dsc.get('pair')
    days_history = dsc.get('days_history')
    exchange = dsc.get('exchange')

    # return live data from cryptocompare ((historical and/or realtime))
    return cc.load_dataframe(pair, days_history, exchange)

def get_live_data_binance():
    pair = dsb.get('pair')
    period = dsb.get('period')
    limit = dsb.get('limit')

    # return live data from binance ((historical and/or realtime))
    return bn.load_dataframe(pair, period, limit)



