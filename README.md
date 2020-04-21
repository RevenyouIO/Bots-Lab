# Bot-Backtesting

Open Source Backtesting Tool. With this tool you can test your bot with historical data to see how it performs.
The results will be compared against the benchmark. See `bots/bot_template.py` and `config_test.py`
for more information.

This project also allows you to create a bot that runs "live", e.g. a bot that sends signals to buy and sell 
based on actual data. To run a bot in live mode, run it on a (virtual) server. A Linux-based server is usually 
the cheapest and most efficient option. 

The following guidelines apply for a Linux-based server: 

* The server should have a recent 64-bit version of Ubuntu Linux as its operating system. Using version 18.04
  or 20.04 (when it becomes available) is recommended.
* The server should have at least 1 GB of memory and 20 GB of disk space.
* You need to have administrative access (via root or sudo) to the server via a terminal (e.g SSH). 

If you want to run the bot on a server your own infrastructure contact your systems or network administrator.  
You can order suitable virtual machines from the following companies:

* DigitalOcean: https://www.digitalocean.com/products/droplets/
* Microsoft: https://azure.microsoft.com/en-us/services/virtual-machines/

Once you have a server available, follow the instructions in the first section to allow it to run this project.

This README contains the following:

* Instructions to get a development and live environment up and running.
  See [Preparing your development or live environment](#preparing-your-development-or-live-environment).

* Instructions to create your own bot.
  See [Create and run your own bot](#create-and-run-your-own-bot).


# Preparing your development or live environment

To run an existing bot or to create your own, you will need to prepare your computer to allow this project
to run. To do this, follow the instructions in this section.

For instructions to create your own bot, see [Create and run your own bot](#create-and-run-your-own-bot).

## Recommended: running the bot using Docker
The easiest way to get up and running is by using Docker. When using Docker, you won't have to install any
platform-specific dependencies (e.g. Python). Only Docker itself is required.

1. If necessary, install Docker.
 
   On Windows and macOS: install Docker Desktop from https://www.docker.com/get-started.
   
   On Ubuntu Linux: install Docker and Docker Compose using the instructions on the following pages:
  
   * https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04
   * https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04
      
   These instructions should also apply for servers from other suppliers. A Docker Hub account is not required. 
   
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
   
* In **live mode**, the bot runs periodically in the background. By default the bot runs every 30 minutes. 
  Also, the bot will start automatically when Docker starts. To show output from the bot, run `docker logs docker_bot_1`.

* To **stop the bot in live mode**, run `./run_bot.sh stop_live` or `run_bot.cmd stop_live`.

* You can add **extra dependecies** by adding them to the `requirements.txt` file. See the remark below.

* After changing any of the files (see [Create and run your own bot](#create-and-run-your-own-bot) below),
  run the test command from the table above again to test your changes. To update the live version with your
  changes, run the `stop_live` command and start the live version again.

## Alternative: running the bot without Docker
If Docker is unavailable for your platform, or if you prefer not to use it, follow
the instructions below to manually install the dependencies required to run a bot.

### Download and install Python 3
For this project Python 3 is needed. Mac users take note: Python is already installed 
as part of your operating system, but this will not suffice. 
For downloading Python 3 see [Download Python](https://www.python.org/downloads/).

*Note:* On Windows, download and install the 32-bit version of Python (this is the default
download option). This makes installing TA-Lib easier.

### Install library TA-Lib
TA-Lib is widely used by trading software developers for perform technical analysis 
of financial market data. Before you can use TA-Lib from Python you must first install the 
underlying TA-Lib library.

To install the underlying dependency TA-lib: 

* On Mac OS: install TA-lib using Brew: `brew install ta-lib`
* On Linux, follow the instructions on [installing TA-Lib from source](https://github.com/mrjbq7/ta-lib#linux).
* On Windows, download prebuilt Python packages (wheels) of TA-Lib for your Python version from
  https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib and place them in the `wheels` folder.

For more information:

* [TA-Lib: Technical Analysis Library](https://ta-lib.org/)
* [TA-Lib Python package GitHub page](https://github.com/mrjbq7/ta-lib)

### Install Python dependencies
On Linux and macOS: run `bash create_venv.sh` from a terminal. On Windows run `create_venv.cmd`.

These scripts will create a virtual Python environment in the directory `venv` below the project directory.
This virtualenv contains all required Python dependencies. They are listed in `requirements.txt`.
After adding extra dependencies to this file you must run `bash create_venv.sh` or `create_venv.cmd` again.  

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

For a basic introduction to use the most common editors available on macOS and Linux, see this article:
https://www.linux.com/topic/desktop/introduction-text-editors-get-know-nano-and-vim/

# Create and run your own bot

This project uses by default a simple bot based on the RSI (Relative Strength Index) algorithm. 
You can find this bot in `bots/rsi.py`. This `bots` folder also contains `ema.py` and 
`sma.py`, two bots that use the Ta-Lib library. To create your own bot, follow the 
instructions in this section of the README.

## Writing your first bot
See `bots/bot_template.py` for an explanation about writing your first bot. 
This means you have to implement the function `get_buy_or_sell_signal` and store that 
function in a python file (extension `.py`) in the `bots` folder.

## Configuration Backtesting tool
See `config_test.py` for the simulation parameters of the Backtesting tool and the data settings for 
the historical data. 

## Run your bot against the backtesting engine
Steps:
1. In `config_test.py` give the parameter `bot_name` the right value: `bot_name = 'bots.[file_name_of_bot]'`
2. Execute the bot in testing mode using the instructions above, e.g. with the recommended Docker command:
   `run_bot.sh test` (or `run_bot.cmd test` on Windows).

## Run your bot live
Steps:
1. In `config_live.py` give the parameter `bot_name` the right value: `bot_name = 'bots.[file_name_of_bot]'`
2. If needed, change the interval in the configuration file `docker/bot/supercronic.conf`
2. Execute the bot in live mode using the instructions above, e.g. with the recommended Docker command:
   `run_bot.sh live` (or `run_bot.cmd live` on Windows).