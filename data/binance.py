import logging
import time

import pandas as pd
import requests

logger = logging.getLogger(__name__)


def get_now(symbol):
    """
    param symbol: market pair
    return: 24 hour ticket data
    """

    params = {
        'symbol': symbol,
    }

    response = requests.get('https://api.binance.com/api/v3/ticker/24hr', params=params).json()
    return response.json()


def get_past(symbol, interval, days_history=30, limit=600):
    """
    param symbol: market pair
    param interval: period of the candles
    param limit: maximum number of candles to be returned
    return: historical charts data from api.binance.com
    """
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    response = requests.get('https://api.binance.com/api/v3/klines', params=params)
    return response.json()

def load_dataframe(symbol, interval, limit=100):
    """
    Return historical charts data from api.binance.com
    param symbol: market pair
    param period: period of the candles
    param limit: maximum number of candles to be returned
    return: histtorical data in the form of a pandas Dataframe
    """
    try:
        data = get_past(symbol, interval, limit)
    except Exception as ex:
        raise ex

    if 'error' in data:
        raise Exception("Bad response: {}".format(data['error']))

    print(data)
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 
        'volume', 'close_time', 'qa_volume', 'trades', 'tbba_volume', 'tbqa_volume', 'ignore'])
    df['date'] = pd.to_datetime(df['date'], unit='ms')

    return df
