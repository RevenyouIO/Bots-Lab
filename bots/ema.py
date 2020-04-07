import talib

def get_buy_or_sell_signal(data):
    """
    Main algorithm method, which will be called every tick.
    (Exponential Moving Average)

    param data: a DataFrame containing a list of candles
    """
    SHORT = 5
    LONG = 30
    MA_FUNC = talib.EMA

    if len(data) < LONG:
        # Skip short history
        return

    short = MA_FUNC(data['close'].values, timeperiod=SHORT)
    long = MA_FUNC(data['close'].values, timeperiod=LONG)

    if short[-1] > long[-1] and short[-2] < long[-2]:
        return 'buy'
    elif short[-1] < long[-1] and short[-2] > long[-2]:
        return 'sell'
    else:
        return None
    
