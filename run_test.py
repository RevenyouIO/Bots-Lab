import importlib

from youengine.youengine import YouEngine
from youengine.helpers.analyze import analyze_mpl, analyze_bokeh
from config_test import sim_params, datasource, bot_name, data_settings_list_poloniex, data_settings_list_cryptocompare, data_settings_list_binance
from data.data_service import get_historical_data_poloniex, get_historical_data_cryptocompare, get_historical_data_binance

def import_bot(name):
    try:
        return importlib.import_module(name)
    except ImportError:
        raise Exception(f'Bot module {name} does not exist')

def get_data_settings_list():
    data_settings_list = None
    if datasource == 'poloniex':
        data_settings_list = data_settings_list_poloniex
    elif datasource == 'cryptocompare':
        data_settings_list = data_settings_list_cryptocompare
    elif datasource == 'binance':
        data_settings_list = data_settings_list_binance

    return data_settings_list

# Request historical data from datasource Poloniex, Cryptocompare or Binance
def get_historical_data(data_settings):
    historical_data = None
    if datasource == 'poloniex':
        historical_data = get_historical_data_poloniex(data_settings_poloniex=data_settings)
    elif datasource == 'cryptocompare':
        historical_data = get_historical_data_cryptocompare(data_settings_cryptocompare=data_settings)
    elif datasource == 'binance':
        historical_data = get_historical_data_binance(data_settings_binance=data_settings)

    return historical_data

# init YouEnigine with simulation parameters and an analysing tool
youengine = YouEngine(sim_params=sim_params, analyze=analyze_bokeh)

# get the bot
bot = import_bot(name = bot_name)

# start backtesting the bot with different pairs (multipair trading)
data_settings_list = get_data_settings_list()
capital_base = sim_params.get('capital_base', 10e5)
for data_settings in data_settings_list:
    historical_data = get_historical_data(data_settings=data_settings)
    if historical_data is None:
        continue
    pair = ''.join(data_settings.get('pair'))
    perf = youengine.run(data=historical_data, bot=bot.get_buy_or_sell_signal, capital_base=capital_base, pair=pair, show_trades=True)
    capital_base = perf['equity'][-1]
