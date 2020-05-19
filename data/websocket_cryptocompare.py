import websocket
import json
import pandas as pd
import time
from datetime import datetime
try:
    import thread
except ImportError:
    import _thread as thread

from config_live import data_settings_cryptocompare
from api_service import send_request

class CryptocompareWebsocketClient:

    def __init__(self, get_buy_or_sell_signal):
        self.ticker_data_array = []
        self.previous_tick = int(round(time.time() * 1000))
        self.get_buy_or_sell_signal = get_buy_or_sell_signal
        self.bot_function_interval = data_settings_cryptocompare.get('bot_function_interval')
        self.max_length_ticker_data_array = data_settings_cryptocompare.get('max_length_ticker_data_array')

    def on_message(self, ws, message):
        ticker_data = json.loads(message)

        # skip this message if it contains no ticker data
        print(ticker_data)
        print(len(ticker_data.keys()))
        if ticker_data['TYPE'] != '2':
            return

        # append ticker data to array and limit size if necessary
        self.ticker_data_array.append(ticker_data)
        if len(self.ticker_data_array) > self.max_length_ticker_data_array:
            self.ticker_data_array.pop(0)
        
        # don't call the bot function when this tick is too soon
        current_tick = int(round(time.time() * 1000))
        interval_between_ticks = current_tick - self.previous_tick
        if interval_between_ticks < self.bot_function_interval:
            return
        self.previous_tick = current_tick

        # print(self.ticker_data_array)
        # get buy or sell signal
        df = self.createDataFrame()
        print(df)
        buy_or_sell_signal = self.get_buy_or_sell_signal(data=df)
        print(buy_or_sell_signal)

        # for now the revenyou api accepts only buy signals!
        if buy_or_sell_signal == 'buy':
            send_request()

    def createDataFrame(self):
        df = pd.DataFrame(self.ticker_data_array)
        df['LASTUPDATE'] = pd.to_datetime(df['LASTUPDATE'], unit='ms')
        df.rename(columns={'LASTUPDATE': 'date', 'OPENDAY': 'open', 'PRICE': 'close', 'HIGHDAY': 'high', 'LOWDAY': 'low', 'VOLUMEDAY': 'volume'}, inplace=True)
        df = df.set_index(['date'])

        columns = ['open', 'close', 'high', 'low', 'volume']
        for column in columns:
            df[column] = df[column].astype(float)

        return df


    def on_error(self, ws, error):
        print("Websocker error: {}", error)

    def on_close(self, ws):
        print("Websocket closed")

    def on_open(self, ws):
        subscribe_request =  {
            "action": "SubAdd",
            "subs": data_settings_cryptocompare.get('pair'),
        }
        ws.send(json.dumps(subscribe_request))

    def listen(self):
        websocket.enableTrace(True)
        uri = 'wss://streamer.cryptocompare.com/v2?api_key={}'.format(data_settings_cryptocompare.get('api_key'))
        ws = websocket.WebSocketApp(uri,
                                on_message = lambda ws,msg: self.on_message(ws, msg),
                                on_error   = lambda ws,msg: self.on_error(ws, msg),
                                on_close   = lambda ws: self.on_close(ws),
                                on_open    = lambda ws: self.on_open(ws))
        ws.on_open = lambda ws: self.on_open(ws)
        ws.run_forever() 