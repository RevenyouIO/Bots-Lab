def get_buy_or_sell_signal(data):
    """
    Main algorithm method based on the relative strength index (RSI), which will be called every tick.
    See also https://www.marketvolume.com/technicalanalysis/rsi.asp

    Param data: a DataFrame containing a list of candles

    TODO: combine RSI with volume surges
    """
    if len(data) < 15:
        # skip because list is too short
        return

    # calculate current RSI
    increase = 0
    decrease = 0
    for x in range(1, 15):
        candle = data.iloc[x * -1]
        difference = candle['close'] - candle['open']
        if difference > 0:
            increase += difference
        elif difference < 0:
            decrease += abs(difference)
    
    current_relative_strength_index = 100 - (100 / ( 1 + (increase / 14) / (decrease / 14) ))

    # calculate previous RSI
    increase = 0
    decrease = 0
    for x in range(2, 16):
        candle = data.iloc[x * -1]
        difference = candle['close'] - candle['open']
        if difference > 0:
            increase += difference
        elif difference < 0:
            decrease += abs(difference)
    
    previous_relative_strength_index = 100 - (100 / ( 1 + (increase / 14) / (decrease / 14) ))

    # close position when RSI breaks the 70 boundary going down
    if current_relative_strength_index < 70 and previous_relative_strength_index > 70:
        return 'sell'
    # open position when the rsi breaks the 30 boundary going up
    elif current_relative_strength_index > 30 and previous_relative_strength_index < 30:
        return 'buy'
    else:
        return None