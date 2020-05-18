# imports of needed libraries come here

def get_buy_or_sell_signal(data):
    """
    Main algorithm method (the actual bot!), which will be called every tick. 
    This method receives a Pandas DataFrame(data). Each row of this Dataframe is a candle. 
    Rows of a DataFrame are dictionary like objects. To access a row value you can use 
    the follwing syntax: row_name['column_name']. Based upon this DataFrame the bot must 
    make a decision to buy, sell or do nothing. See below for a simple example.

    Param data: 
    List of candles or ticker data in the form of a Pandas Dataframe. The test environment
    uses candles (historical data) and the live environment ticker data. Candles or ticker data 
    have minimal the following properties: date, open, high, low, close and volume.

    Example candle / ticker data:
    date                open       high       low        close       volume      date
    2020-03-03 12:00:00 0.02608580 0.02613449 0.02581001 0.02581078  59.40688146 2020-03-03 12:00:00

    Return: 'buy', 'sell' or None
    """

    # skip when the number of rows (candles) is too short
    if len(data) < 2:
        return None

    # get the last and second to last row
    current_candle = data.iloc[-1]
    previous_candle = data.iloc[-2]

    # return sell signal
    if current_candle['close'] < previous_candle['close']:
        return 'sell'

    # return buy signal
    elif current_candle['close'] > previous_candle['close']:
        return 'buy'
