from youengine.youengine import YouEngine
from youengine.helpers.analyze import analyze_mpl, analyze_bokeh
from config_test import sim_params, datasource
from data.data_service import get_historical_data_poloniex, get_historical_data_cryptocompare
# choose here which bot to import
from rsi import get_buy_or_sell_signal

# Request historical data from datasource Poloniex or Cryptocompare
historical_data = None
if datasource == 'poloniex':
    historical_data = get_historical_data_poloniex()
elif datasource == 'cryptocompare':
    historical_data = get_historical_data_cryptocompare()

if historical_data is None:
    exit()

# init YouEnigine with simulation parameters and an analysing tool
youengine = YouEngine(sim_params=sim_params, analyze=analyze_bokeh)

# start backtesting the bot with the historical data
youengine.run(data=historical_data, bot=get_buy_or_sell_signal, show_trades=True)