import requests
import uuid
import importlib
import websocket
import json
import pandas as pd
try:
    import thread
except ImportError:
    import _thread as thread
import time

from data.data_service import data_settings_binance

class BinanceWebsocketClient():
    
    def __init__(self):
        self.ticker_data_array = []
        self.previous_tick = 0

    def on_message(ws, message):
        ticker_data = json.loads(message)
        if int(ticker_data['E']) - self.previous_tick < 5000:
            self.previous_tick = int(ticker_data['E'])
            print('too soon')
            return

        self.previous_tick = int(ticker_data['E'])
        print(message)

        self.ticker_data_array.append(ticker_data)
   
      if len(self.ticker_data_array) > 5:
            self.ticker_data_array.pop(0)
        
        df = pd.DataFrame(self.ticker_data_array)
        print('data frame: ')
        print(df)

    def on_error(ws, error):
        print("Websocker error: {}", error)

    def on_close(ws):
        print("Websocket closed")

    def on_open(ws):
        ws.send({
            "method": "SUBSCRIBE",
            "params": [
                "{}@miniTicker".format(data_settings_binance.get('pair').lower()),
            ],
            "id": 1
        })

    def listen():
        websocket.enableTrace(True)
        uri = 'wss://stream.binance.com:9443/ws/{}@miniTicker'.format(data_settings_binance.get('pair').lower())
        ws = websocket.WebSocketApp(uri,
                                  on_message = on_message,
                                  on_error = on_error,
                                  on_close = on_close)
        ws.on_open = on_open
        ws.run_forever()