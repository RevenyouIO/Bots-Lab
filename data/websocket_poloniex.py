import websocket
import json
import pandas as pd
import time
from datetime import datetime

from config_live import data_settings_poloniex
from api_service import send_request

class PoloniexWebsocketClient:

    def __init__(self, get_buy_or_sell_signal):
        self.previous_tick = int(round(time.time() * 1000))
        self.get_buy_or_sell_signal = get_buy_or_sell_signal
        self.bot_function_interval = data_settings_poloniex.get('bot_function_interval')
        self.max_length_ticker_data_array = data_settings_poloniex.get('max_length_ticker_data_array')
        self.currency_id_pair_dictionary = data_settings_poloniex.get('currency_id_pair_dictionary')
        self.ticker_data_dictionary = {}

        self.initialize_ticker_data_dictionary()

    def initialize_ticker_data_dictionary(self):
        for currency_id, pair in self.currency_id_pair_dictionary.items():
            self.ticker_data_dictionary[pair] = []

    def on_message(self, ws, message):
        ticker = json.loads(message)

        # skip this message if it contains no ticker data
        if len(ticker) < 3:
            return

        self.add_ticker_to_ticker_data_dictionary(ticker=ticker)

        # don't call the bot function when this tick is too soon
        current_tick = int(round(time.time() * 1000))
        interval_between_ticks = current_tick - self.previous_tick
        if interval_between_ticks < self.bot_function_interval:
            return
        self.previous_tick = current_tick

        for pair, ticker_data_array in self.ticker_data_dictionary.items():
            df = self.createDataFrame(ticker_data_array=ticker_data_array)
            buy_or_sell_signal = self.get_buy_or_sell_signal(data=df)
            print(buy_or_sell_signal)

            # for now the revenyou api accepts only buy signals!
            if buy_or_sell_signal == 'buy':
                send_request(pair=pair)

    def add_ticker_to_ticker_data_dictionary(self, ticker):
        currency_id = str(ticker[2][0])
        if currency_id in self.currency_id_pair_dictionary:
            ticker_data = ticker[2]
            ticker_data.append(datetime.now())
            pair = self.currency_id_pair_dictionary[currency_id]
            self.ticker_data_dictionary[pair].append(ticker_data)
        
            # limit size ticker data array when it becomes too big
            if len(self.ticker_data_dictionary[pair]) > self.max_length_ticker_data_array:
                self.ticker_data_dictionary[pair].pop(0)

    def createDataFrame(self, ticker_data_array):
        df = pd.DataFrame(ticker_data_array, columns=['pair_id', 'close', 'low_ask', 'high_ask', 'percentage_change', 'volume', 
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
        print("Websocket is closed")

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