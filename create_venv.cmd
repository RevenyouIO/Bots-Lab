@ECHO OFF

REM Check if pip3 is installed
WHERE /Q pip3
IF ERRORLEVEL 1 (
    ECHO The pip3 command is not installed or not on PATH. Please install Python 3.8 and ensure the python and pip3 commands are available are on the PATH.
    EXIT /B
)

REM Check if virtualenv is installed
WHERE /Q virtualenv
IF ERRORLEVEL 1 (
    ECHO Installing virtualenv using PIP...
    pip3 install virtualenv    
)

virtualenv venv

venv\scripts\pip3 install -r requirements.txt --find-links wheels
