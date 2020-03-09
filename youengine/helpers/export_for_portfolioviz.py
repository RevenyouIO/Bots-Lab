import pandas as pd

from youengine.helpers import cryptocompare as cc

pair = ['BTC', 'USD']  # Use ETH pricing data on the BTC market
daysBack = 0  # Grab data starting X days ago
daysData = 365 * 5  # From there collect X days of data
# Exchange = 'Bitstamp'
# Request data from cryptocompare
data = cc.get_past(pair, daysBack, daysData, Exchange='CCCAGG')

# Convert to Pandas dataframe with datetime format
data = pd.DataFrame(data)
data = data.set_index(['time'])
data.index = pd.to_datetime(data.index, unit='s')
# data['date'] = pd.to_datetime(data['time'], unit='s')
data_MS = data.resample('M').last()
# print(data1)
data_MS['Period'] = data_MS.index.strftime('%Y-%m')
data_MS['Return'] = data_MS['close'].pct_change()
csv_out = data_MS.to_csv(columns=['Period', 'Return'])
print(csv_out)
