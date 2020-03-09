# Bot-Backtesting
Open Source Backtesting Tool.

## Download Python
For downloading Python see [Download Python](https://www.python.org/downloads/).

## Installing Pip
Pip is the recommended package manager for installing libraries. 
For installing Pip see [Install Pip](https://pypi.org/project/pip/).

### User guide with Pip
For a user guide see [User guide Pip](https://pip.pypa.io/en/stable/user_guide/).

### Install libraries with requirements.txt
With the command `pip install -r requirements.txt` you can install multiple libraries at once.
See the requirement.txt file for the libraries needed in this project. When you have installed
python 3 on the Mac run: `pip3 install -r requirements.txt`.

Before you can install TA-Lib you must first install the underlying depency ta-lib. For example 
on the Mac you must first execute the command `brew install ta-lib`. 
Only then can you install TA-Lib.

## Create and run your first bot

### Write bot
See the botsjabloon.py for an explanation about writing your first bot. 
This means you have to implement the function `get_buy_or_sell_signal`.

### Config test
See `config_test` for the simulation parameters of the backtesting engine and the data settings for 
the historical data.

### Run your bot against the backtesting engine
First you ahve to import the bot you have written through an import statement:
`from [file_name_of_bot_function] import get_buy_or_sell_signal`
Execute the following command on the command line: `python run_test.py`. When you have installed
python 3 on the Mac run: `python3 run_test.py`.
