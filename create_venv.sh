#!/bin/bash

PROJECT_DIR=$(dirname "$0")
PYTHON3_INTERPRETER="$(command -v python3)"
PIP3_TOOL="$(command -v pip3)"
PROJECT_VENV="$PROJECT_DIR/venv"

function check_python() {
# Check if Python 3 is installed
  if [ -z "$PYTHON3_INTERPRETER" ] ; then
    echo "Python 3 is not installed, or it is not on the PATH."
    echo "Please install Python 3.7 or higher, see https://www.python.org"
    exit 1
  fi
}

function check_virtualenv_tool() {
  # Check if virtualenv is installed
  VIRTUALENV_TOOL="$(command -v virtualenv)"
  if [ -z "$VIRTUALENV_TOOL" ] ; then
    echo "The virtualenv tool is not installed, or it is not on the PATH."

    if [ -z "$PIP3_TOOL" ] ; then
      echo "PIP is not installed, or it is not on the PATH."
      echo "Please install virtualenv yourself."
      exit 2
    else
      echo "Trying to install virtualenv using PIP"
      set -e
      "$PIP3_TOOL" install virtualenv
      set +e
      echo "virtualenv has been installed succesfully"
    fi
  fi
}

function create_virtualenv() {
  if [ ! -e "$PROJECT_VENV" ] ; then
    set -e
    VIRTUALENV_TOOL="$(command -v virtualenv)"
    "$VIRTUALENV_TOOL" -p "$PYTHON3_INTERPRETER" "$PROJECT_VENV"
    set +e
  else
    echo "Virtual environment already exists, not creating."
  fi
}

function install_requirements() {
  set -e
  "$PROJECT_VENV/bin/pip3" install -r "$PROJECT_DIR/requirements.txt"
}

check_python
check_virtualenv_tool
create_virtualenv
install_requirements

echo
echo "Virtual environment has been created at $PROJECT_VENV."
echo "Activate using . $PROJECT_VENV/bin/activate"
echo