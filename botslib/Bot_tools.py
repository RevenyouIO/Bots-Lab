##############################################
# Bot_tools.py
# Support functions for BotCreator notebooks
# contact: philip@revenyou.io
# (C) Bots by RevenYOU
##############################################

# Read the sample data
import pandas as pd
def read_historical_data():
    data = pd.read_csv("btc_eth_1800_100.csv",header=0, index_col=0)
    data.index = pd.to_datetime(data.index)
    columns = ["high", "low", "open", "close"]
    return data[columns]

# Plot OHLC bars
import mplfinance as mplf
def plot_bars(bars: pd.DataFrame):
    mplf.plot(bars,type='candle')

# Calc moving average from data list using timeperiod = period
import talib
def calc_sma(data, period):
    MA_FUNC = talib.SMA

    if(len(data) < period):
        return

    ma_list = MA_FUNC(data, timeperiod=period)
    return ma_list

# Plot a series of lines
import pandas as pd
def plot_lines(data, labels, start, end):
    plotDF = pd.concat([pd.Series(x) for x in data], axis = 1)
    plotDF.columns = labels

    plotDF[start:end].plot.line()
