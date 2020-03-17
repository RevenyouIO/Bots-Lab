# Bot-Backtesting
Open Source Backtesting Tool.
With this tool you can test your bot with historical data to see how it performs.
The results will be compared against the benchmark. See botsjabloon.py and config_test.py
for more information.

## Download Python 3
For this project Python 3 is needed. Mac users take note: Python is allready installed 
as part of your operating system, but this will not suffice. 
For downloading Python 3 see [Download Python](https://www.python.org/downloads/).


## Pip package manager
Pip is the recommended package manager for installing libraries. 
For more information about Pip see [Pip home page](https://pypi.org/project/pip/)

### Install Pip
Pip should allready be installed when downloading Python. But if somehow it is not 
see [Install Pip](https://pip.pypa.io/en/stable/installing/) for installing Pip.

### User guide Pip
For a user guide see [User guide Pip](https://pip.pypa.io/en/stable/user_guide/).

## Install libraries

### Install library TA-Lib
Before you can install TA-Lib you must first install the underlying dependecy ta-lib. For example 
on the Mac, when you have installed brew, you must first execute the command `brew install ta-lib`. 
Only then can you install TA-Lib.

### Install libraries globally with requirements.txt
Steps:
1. Go to the root directory of the project
2. Run the command `pip install -r requirements.txt` (on the Mac: `pip3 install -r requirements.txt`).

### Install libaries locally for your project with requirements.txt
Steps:
1. Install virtualenv (this still has to be done globally): `pip3 install virtualenv`
2. Go to the root directory of the project
2. Create a virtualenv in your project: `virtualenv venv`
3. activate virtualenv: `. venv/bin/activate`
4. Install the requirements: `pip3 install -r requirements.txt` (on the Mac: `pip3 install -r requirements.txt`).

## Create and run your first bot

### Write bot
See the botsjabloon.py for an explanation about writing your first bot. 
This means you have to implement the function `get_buy_or_sell_signal` and store that 
function in a python file (extension .py). For an example see rsi.py.

### Config test
See `config_test` for the simulation parameters of the Backtesting tool and the data settings for 
the historical data. 

### Run your bot against the backtesting engine
Steps:
1. First you have to import the `get_buy_or_sell_signal` function that you have written. 
You can can do that by going to the `run_test.py` file. Fill in the name of the file that contains your 
`get_buy_or_sell_signal` function: `from [file_name_of_bot_function] import get_buy_or_sell_signal`.
2. Then you can execute the following command on the command line: `python run_test.py`. 
On the Mac : `python3 run_test.py`.
