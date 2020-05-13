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

from data.data_service import data_settings_binance

class BinanceWebsocketClient:
    
    def __init__(self):
        self.ticker_data_array = []
        self.previous_tick = 0

    def on_message(self, ws, message):
        ticker_data = json.loads(message)

        # skip this tick when it is too soon
        if (int(ticker_data['E']) - self.previous_tick) < 5000:
            return

        self.previous_tick = int(ticker_data['E'])

        print(message)

        self.ticker_data_array.append(ticker_data)
   
        # limit the ticker data array size
        if len(self.ticker_data_array) > 20:
            self.ticker_data_array.pop(0)
        
        df = pd.DataFrame(self.ticker_data_array)
        df['E'] = pd.to_datetime(df['E'], unit='ms')
        df.columns = ['type', 'date', 'symbol', 'close', 'open', 'high', 'low', 'volume', 'volume_quote']

        # roep bot aan, en stuur eventueel buy signal
        print('data frame: ')
        print(df)

    def on_error(self, ws, error):
        print("Websocker error: {}", error)

    def on_close(self, ws):
        print("Websocket closed")

    def on_open(self, ws):
        ws.send({
            "method": "SUBSCRIBE",
            "params": [
                "{}@miniTicker".format(data_settings_binance.get('pair').lower()),
            ],
            "id": 1
        })

    def listen(self):
        websocket.enableTrace(True)
        uri = 'wss://stream.binance.com:9443/ws/{}@miniTicker'.format(data_settings_binance.get('pair').lower())
        ws = websocket.WebSocketApp(uri,
                                on_message = lambda ws,msg: self.on_message(ws, msg),
                                on_error   = lambda ws,msg: self.on_error(ws, msg),
                                on_close   = lambda ws: self.on_close(ws),
                                on_open    = lambda ws: self.on_open(ws))
        ws.on_open = lambda ws: self.on_open(ws)
        ws.run_forever()