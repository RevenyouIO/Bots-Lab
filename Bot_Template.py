# LIBRARIES


from binance.client import Client
import pandas as pd
import json
import time
import ta
from math import *
from datetime import datetime
import uuid
import botslib.bots_api as ba
import ccxt
import config
from sys import set_coroutine_origin_tracking_depth
import numpy as np
import json
from ta.volatility import BollingerBands, AverageTrueRange
import schedule


#TO BE ABLE TO USE BA/botslib.bots_api, YOU WILL HAVE TO CLONE THE GITHUB REPO - https://github.com/RevenyouIO/Bots-Lab


#BOTS API URL - PAPER MODE - USE THE URL BELOW  IN ORDER  TO DEVELOP AND TEST YOUR BOT

bots_platform = ba.BEM_API('https://signal.revenyou.io/paper/api/signal/v2/')


#BINANCE API FOR DATA STREAM

exchange = ccxt.binanceus({
"apiKey": 'YOUR_BINANCE_API' ,
 "secret": 'YOUR_SECRET_KEY'
})



#The get_buy_sell_signals function makes the order requests when it sees a signal based on the strategy.

#ba.OrderParameters is used to set the mandatory parameters you will need to make the order request
#bots_platform.placeOrder function is used to make the order request



in_position = False

def get_buy_or_sell_signal(data):
    global in_position

    print("checking for signals")
    print(data.tail(10))

    if data['EMA28'].iloc[-2] > data['EMA48'].iloc[-2] and data['STOCH_RSI'].iloc[-2] < 0.8:       
        print('Will buy if not in position')
        if not in_position:
            limitBuy = str(df['high'].iloc[-1]*1.1)
            #setting order
            order = ba.OrderParameters(signalProvider='BOT_NAME',
                                       signalProviderKey='API_KEY',
                                       extId=str(uuid.uuid4()),
                                       exchange='binance',
                                       baseAsset='BTC',
                                       quoteAsset='USDT',
                                       side='buy',
                                       limitPrice=limitBuy,
                                       qtyPct='100',
                                       ttlType='secs',
                                       ttlSecs=str(40))
            print(json.loads(bots_platform.placeOrder(order)))
            state_request = ba.OrderStateRequest(signalProvider='BOT_NAME',signalProviderKey='BOT_KEY, extId =order.extId)
            position_request = ba.PositionRequest(signalProvider='BOT_NAME',signalProviderKey='API_KEY',exchange='binance', baseAsset='USDT')



            in_position = True

        else:
            print("already in position, nothing to do")

    if data['EMA28'].iloc[-2] < data['EMA48'].iloc[-2] and data['STOCH_RSI'].iloc[-2] > 0.2:
        if in_position:
            print("Time to close")
            limitSell = str(df['low'].iloc[-1]*0.9)
            order = ba.OrderParameters(signalProvider='BOT_NAME',
                                       signalProviderKey='API_KEY',
                                       extId=str(uuid.uuid4()),
                                       exchange='binance',
                                       baseAsset='BTC',
                                       quoteAsset='USDT',
                                       side='sell',
                                       limitPrice=limitSell,
                                       qtyPct='100',
                                       ttlType='secs',
                                       ttlSecs=str(40))
            print(json.loads(bots_platform.placeOrder(order)))
            state_request = ba.OrderStateRequest(signalProvider='BOT_NAME', signalProviderKey='API_KEY', extId = order.extId)
            position_request = ba.PositionRequest(signalProvider='BOT_NAME',signalProviderKey='API_KEY',exchange='binance', baseAsset='USDT')
            #bot.sendMessage(receiver_id, bots_platform.getOrderState(state_request))
            #bot.sendMessage(receiver_id,bots_platform.getBotAssetsPct(position_request))
            
            in_position = False

        else:
             print("You aren't in position, nothing to sell")



###THIS IS THE ACTUAL BOT. THIS FUNCTION CONTINUOUSLY FETCHES DATA AND APPLIES TECHNICAL INDICATORS ON THE FETCHED DATA EVERY 10 SECONDS.


def run_bot():

    print(f"Fetching new bars for {datetime.now().isoformat()}")
    bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='1m', limit=100)
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['TRIX'] = ta.trend.ema_indicator(ta.trend.ema_indicator(ta.trend.ema_indicator(close=df['close'], window=trixLength), window=trixLength), window=trixLength)
    df['TRIX_PCT'] = df["TRIX"].pct_change()*100
    df['TRIX_SIGNAL'] = ta.trend.sma_indicator(df['TRIX_PCT'],trixSignal)
    df['TRIX_HISTO'] = df['TRIX_PCT'] - df['TRIX_SIGNAL']
    df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=15,smooth1=3, smooth2=3)
    df['EMA28']=ta.trend.ema_indicator(df['close'], 1)
    df['EMA48']=ta.trend.ema_indicator(df['close'], 3)
    
    Bot_data = df
    
    get_buy_or_sell_signal(df)

schedule.every(10).seconds.do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(1)
