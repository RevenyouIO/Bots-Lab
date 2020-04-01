#!/bin/bash

if [ -z "$(command -v docker-compose)" ] ; then
  echo "Please install Docker and Docker Compose to use this script"
  exit 1
fi

MODE="$1"

if [ "$MODE" == "test" ] ; then
  docker-compose -f docker/docker-compose-test.yml up --build
elif [ "$MODE" == "live" ] ; then
  docker-compose -f docker/docker-compose-live.yml up --build -d
elif [ "$MODE" == "stop_live" ] ; then
  docker-compose -f docker/docker-compose-live.yml down
else
  echo "Run this script with one of the following arguments: test, live, stop_live"
fi
