# Bot-Backtesting

Open Source Backtesting Tool. With this tool you can test your bot with historical data to see how it performs.
The results will be compared against the benchmark. See `bot_template.py` and `config_test.py`
for more information.

This project also allows you to create a bot that runs "live", e.g. a bot that sends signals to buy and sell 
based on actual data.

This file contains instructions to get a development environment up and running
(see first and second section)

# Getting up and running
 
## Recommended: running the bot using Docker
The easiest way to get up and running is by using Docker. When using Docker, you won't have to install any
platform-specific dependencies (e.g. Python). Only Docker itself is required.

1. If necessary, install Docker from https://www.docker.com/
2. Clone the Bot-Backtesting project to your computer using Git if you haven't already done so. 
3. Open a command prompt, `cd` to the project directory and run one of the following commands:

   | Platform        | Testing mode            | Live mode              |
   | --------------- | ----------------------  | ---------------------- |
   | macOS and Linux | `./run_bot.sh test`     | `./run_bot.sh live`    |
   | Windows         | `run_bot.cmd test`      | `run_bot.cmd live`     |
   
Remarks:

* When running one of these commands for the first time, a Docker image will be built for the bot. 
  This may take a few minutes and produce a lot of output. Next runs will be faster and quieter.

* In **testing mode**, the bot runs once and exits automatically. Output is shown immediately.
   
* In **live mode**, the bot runs periodically in the background. Also, the bot will start automatically when Docker 
  starts. To show output from the bot, run `docker logs docker_bot_1`.

* To **stop the bot in live mode**, run `./run_bot.sh stop_live` or `run_bot.cmd stop_live`.

* After changing any of the files (see [Create and run your first bot](#create-and-run-your-first-bot) below),
  run the test command from the table above again to test your changes. To update the live version with your
  changes, run the `stop_live` command and start the live version again.

## Alternative: running the bot without Docker
If Docker is unavailable for your platform, or if you prefer not to use it, follow
the instructions below to manually install the dependencies required to run a bot.

### Download and install Python 3
For this project Python 3 is needed. Mac users take note: Python is already installed 
as part of your operating system, but this will not suffice. 
For downloading Python 3 see [Download Python](https://www.python.org/downloads/).

### Install library TA-Lib
TA-Lib is widely used by trading software developers for perform technical analysis 
of financial market data. Before you can install TA-Lib you must first install the 
underlying dependency ta-lib. Only then can you install TA-Lib. 

On macOS, you can install TA-Lib using Homebrew: `brew install ta-lib`

On Linux, follow the instructions on [installing TA-lib from source](https://github.com/mrjbq7/ta-lib#linux).

For more information see [GitHub TA-Lib](https://github.com/mrjbq7/ta-lib)

### Install Python dependencies
On Linux and macOS: run `bash create_venv.sh` from a terminal. This script will
create a virtual Python environment in the directory `venv` below the project directory.
This virtualenv contains all required Python dependencies.

### Running the bot in test mode

On macOS and Linux: `venv/bin/python3 run_test.py`

On Windows: `venv\scripts\python3 run_test.py`

### Running the bot in live mode

To run the bot in live mode, you will need to schedule a task that periodically runs your bot.
This can be done using `cron` on macOS and Linux:

* Run the following command to start editing the cron file of the current user:
  `crontab -e`
  
* Add the following lines, replacing `/path/to/project` with the path to the project:

  ```
  # Run bot every 30 minutes:
  */30 * * * *   /path/to/project/venv/bin/python3 /path/to/project/run_live.py 
  ```

* Save the file and exit the editor.  

# Create and run your first bot

## Writing your first bot
See the `bot_template.py` for an explanation about writing your first bot. 
This means you have to implement the function `get_buy_or_sell_signal` and store that 
function in a python file (extension `.py`). For an example see `rsi.py`.

## Configuration Backtesting tool
See `config_test.py` for the simulation parameters of the Backtesting tool and the data settings for 
the historical data. 

## Run your bot against the backtesting engine
Steps:
1. In `config_test.py` give the parameter `bot_name` the right value: `bot_name = '[file_name_of_bot]'`
2. Execute the bot in testing mode using the instructions above, e.g. with the recommended Docker command:
   `run_bot.sh test` (or `run_bot.cmd test` on Windows).

## Run your bot live
Steps:
1. In `config_live.py` give the parameter `bot_name` the right value: `bot_name = '[file_name_of_bot]'`
2. If needed, change the interval in the configuration file `docker/bot/supercronic.conf`
2. Execute the bot in live mode using the instructions above, e.g. with the recommended Docker command:
   `run_bot.sh live` (or `run_bot.cmd live` on Windows).