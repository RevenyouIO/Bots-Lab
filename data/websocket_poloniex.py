import websocket
import json
import pandas as pd
import time
from datetime import datetime
try:
    import thread
except ImportError:
    import _thread as thread

from config_live import data_settings_poloniex
from api_service import send_request

class PoloniexWebsocketClient:

    def __init__(self, get_buy_or_sell_signal):
        self.ticker_data_array = []
        self.previous_tick = int(round(time.time() * 1000))
        self.get_buy_or_sell_signal = get_buy_or_sell_signal
        self.bot_function_interval = data_settings_poloniex.get('bot_function_interval')
        self.max_length_ticker_data_array = data_settings_poloniex.get('max_length_ticker_data_array')
        self.currency_pair_id = data_settings_poloniex.get('currency_pair_id')

    def on_message(self, ws, message):
        ticker = json.loads(message)

        # skip this message if it contains no ticker data
        if len(ticker) < 3:
            return

        # if the ticker data is of the wright pair append it to the array and continue
        if ticker[2][0] == self.currency_pair_id:
            ticker_data = ticker[2]
            ticker_data.append(datetime.now())
            self.ticker_data_array.append(ticker_data)
        else:
            return
        
        # limit size ticker data array when it becomes too big
        if len(self.ticker_data_array) > self.max_length_ticker_data_array:
            self.ticker_data_array.pop(0)

        # don't call the bot function when this tick is too soon
        current_tick = int(round(time.time() * 1000))
        interval_between_ticks = current_tick - self.previous_tick
        if interval_between_ticks < self.bot_function_interval:
            return
        self.previous_tick = current_tick

        # get buy or sell signal
        df = self.createDataFrame()
        buy_or_sell_signal = self.get_buy_or_sell_signal(data=df)
        print(buy_or_sell_signal)

        # for now the revenyou api accepts only buy signals!
        if buy_or_sell_signal == 'buy':
            send_request()

    def createDataFrame(self):
        df = pd.DataFrame(self.ticker_data_array, columns=['pair_id', 'close', 'low_ask', 'high_ask', 'percentage_change', 'volume', 
            'quote_volume', 'is_frozen', 'high', 'low', 'date'])
        df = df.set_index(['date'])

        columns = ['close', 'low_ask', 'high_ask', 'percentage_change', 'volume', 
            'quote_volume', 'is_frozen', 'high', 'low']
        for column in columns:
            df[column] = df[column].astype(float)

        return df

    def on_error(self, ws, error):
        print("Websocker error: {}", error)

    def on_close(self, ws):
        print("Websocket is automatically closed after 24h, so open it again")
        self.listen()

    def on_open(self, ws):
        subscribe_request =  { "command": "subscribe", "channel": 1002 }
        ws.send(json.dumps(subscribe_request))

    def listen(self):
        websocket.enableTrace(True)
        uri = 'wss://api2.poloniex.com'
        ws = websocket.WebSocketApp(uri,
                                on_message = lambda ws,msg: self.on_message(ws, msg),
                                on_error   = lambda ws,msg: self.on_error(ws, msg),
                                on_close   = lambda ws: self.on_close(ws),
                                on_open    = lambda ws: self.on_open(ws))
        ws.on_open = lambda ws: self.on_open(ws)
        ws.run_forever() 