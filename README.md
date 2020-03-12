# Bot-Backtesting
Open Source Backtesting Tool.

## Download Python 3
For this project Python 3 is needed. Mac users take note: Python is allready installed 
as part of your operating system, but this will not suffice. 
For downloading Python 3 see [Download Python](https://www.python.org/downloads/).


## Pip package manager
Pip is the recommended package manager for installing libraries. 
For more information about Pip see [Pip home page](https://pypi.org/project/pip/)

### Installing Pip
For installing Pip see [Install Pip](https://pip.pypa.io/en/stable/installing/).

### User guide Pip
For a user guide see [User guide Pip](https://pip.pypa.io/en/stable/user_guide/).

### Install library TA-Lib
Before you can install TA-Lib you must first install the underlying dependecy ta-lib. For example 
on the Mac, when you have installed brew, you must first execute the command `brew install ta-lib`. 
Only then can you install TA-Lib.

### Install libraries with requirements.txt
With the command `pip install -r requirements.txt` you can install multiple libraries at once.
See the requirement.txt file for the libraries needed in this project.
Steps:
1. install TA-Lib
2. go to the root directory of the project
3. run the command `pip install -r requirements.txt` (on the Mac open your terminal 
and run: `pip3 install -r requirements.txt`).

## Create and run your first bot

### Write bot
See the botsjabloon.py for an explanation about writing your first bot. 
This means you have to implement the function `get_buy_or_sell_signal` and store that 
function in a python file (extension .py). For an example see rsi.py.

### Config test
See `config_test` for the simulation parameters of the backtesting engine and the data settings for 
the historical data. 

### Run your bot against the backtesting engine
Steps:
1. First you have to import the `get_buy_or_sell_signal` function that you have written. 
You can can do that by going to the `run_test.py` file. Fill in the name of the file that contains your 
`get_buy_or_sell_signal` function: `from [file_name_of_bot_function] import get_buy_or_sell_signal`.
2. Then you can execute the following command on the command line: `python run_test.py`. When you have installed
python 3 on the Mac run in the terminal: `python3 run_test.py`.
