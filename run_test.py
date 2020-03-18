import importlib

from youengine.youengine import YouEngine
from youengine.helpers.analyze import analyze_mpl, analyze_bokeh
from config_test import sim_params, datasource, bot_name
from data.data_service import get_historical_data_poloniex, get_historical_data_cryptocompare

def import_bot(name):
    try:
        return importlib.import_module(name)
    except ImportError:
        raise Exception(f'Bot module {name} does not exist')

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
bot = import_bot(name = bot_name)
youengine.run(data=historical_data, bot=bot.get_buy_or_sell_signal, show_trades=True)