import websocket
import json
import pandas as pd
import logging

from config_live import data_settings_binance
from api_service import send_request

logger = logging.getLogger(__name__)

class BinanceWebsocketClient:
    
    def __init__(self, get_buy_or_sell_signal):
        self.get_buy_or_sell_signal = get_buy_or_sell_signal
        self.max_length_ticker_data_list = data_settings_binance.get('max_length_ticker_data_list')
        self.pair_list = data_settings_binance.get('pair_list')
        self.pair_ticker_data_list_dictionary = {}

        self.initialize_pair_ticker_data_list_dictionary()


    def initialize_pair_ticker_data_list_dictionary(self):
        for pair in self.pair_list:
            self.pair_ticker_data_list_dictionary[pair] = []

    def on_message(self, ws, message):
        ticker = json.loads(message)

        if not 'data' in ticker.keys():
            return

        pair = self.get_pair(ticker=ticker)
        self.store_ticker_data(pair=pair, ticker=ticker)
        self.run_bot(pair=pair)

    def get_pair(self, ticker):
        stream = ticker.get('stream')
        pair = stream.split('@')[0]

        return pair    

    def store_ticker_data(self, pair, ticker):
        ticker_data = ticker.get('data')
        self.pair_ticker_data_list_dictionary[pair].append(ticker_data)

        if len(self.pair_ticker_data_list_dictionary[pair]) > self.max_length_ticker_data_list:
            self.pair_ticker_data_list_dictionary[pair].pop(0)

    def run_bot(self, pair):
        ticker_data_list= self.pair_ticker_data_list_dictionary[pair]
        df = self.create_dataframe(ticker_data_list=ticker_data_list)
        buy_or_sell_signal = self.get_buy_or_sell_signal(data=df)
        logger.debug('buy signal for pair {}: {}'.format(pair, buy_or_sell_signal))


        # for now the revenyou api accepts only buy signals!
        if buy_or_sell_signal == 'buy':
            send_request(pair=pair)

    def create_dataframe(self, ticker_data_list):
        df = pd.DataFrame(ticker_data_list)
        df.columns = ['type', 'date', 'symbol', 'close', 'open', 'high', 'low', 'volume', 'volume_quote']
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        df = df.set_index(['date'])

        columns = ['close', 'open', 'high', 'low', 'volume', 'volume_quote']
        for column in columns:
            df[column] = df[column].astype(float)

        return df

    def on_error(self, ws, error):
        print("Websocker error: {}", error)

    def on_close(self, ws):
        print("Websocket is automatically closed after 24h, so open it again")
        self.listen()

    def on_open(self, ws):
        subscribe_request = {
            "method": "SUBSCRIBE",
            "params": self.get_params_value(),
            "id": 1
        }
        ws.send(json.dumps(subscribe_request))

    def get_params_value(self):
        return [pair + '@miniTicker' for pair in self.pair_list]

    def listen(self):
        websocket.enableTrace(True)
        uri = 'wss://stream.binance.com:9443/stream?streams={}'.format(self.get_streams_value())
        ws = websocket.WebSocketApp(uri,
                                on_message = lambda ws,msg: self.on_message(ws, msg),
                                on_error   = lambda ws,msg: self.on_error(ws, msg),
                                on_close   = lambda ws: self.on_close(ws),
                                on_open    = lambda ws: self.on_open(ws))
        ws.on_open = lambda ws: self.on_open(ws)
        ws.run_forever()

    def get_streams_value(self):
        return '@miniTicker/'.join(self.pair_list)