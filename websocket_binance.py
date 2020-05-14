import websocket
import json
import pandas as pd
try:
    import thread
except ImportError:
    import _thread as thread

from config_live import data_settings_binance
from api_service import send_request

class BinanceWebsocketClient:
    
    def __init__(self, get_buy_or_sell_signal):
        self.ticker_data_array = []
        self.previous_tick = 0
        self.get_buy_or_sell_signal = get_buy_or_sell_signal
        self.bot_function_interval = data_settings_binance.get('bot_function_interval')
        self.max_length_ticker_data_array = data_settings_binance.get('max_length_ticker_data_array')

    def on_message(self, ws, message):
        ticker_data = json.loads(message)

        # skip this message if it is the very first message that contains no ticker data
        if 'result' in ticker_data.keys():
            return

        # skip this tick when it is too soon
        interval_between_ticks = int(ticker_data['E']) - self.previous_tick
        if interval_between_ticks < self.bot_function_interval:
            return
        self.previous_tick = int(ticker_data['E'])

        # append ticker data to array and limit size if necessary
        self.ticker_data_array.append(ticker_data)
        if len(self.ticker_data_array) > self.max_length_ticker_data_array:
            self.ticker_data_array.pop(0)
        
        # get buy or sell signal
        df = self.createDataFrame()
        buy_or_sell_signal = self.get_buy_or_sell_signal(data=df)
        print(buy_or_sell_signal)

        # for now the revenyou api accepts only buy signals!
        if buy_or_sell_signal == 'buy':
            send_request()

    def createDataFrame(self):
        df = pd.DataFrame(self.ticker_data_array)
        df['E'] = pd.to_datetime(df['E'], unit='ms')
        df.columns = ['type', 'date', 'symbol', 'close', 'open', 'high', 'low', 'volume', 'volume_quote']

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
            "params": [
                "{}@miniTicker".format(data_settings_binance.get('pair').lower()),
            ],
            "id": 1
        }
        ws.send(json.dumps(subscribe_request))

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