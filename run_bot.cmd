@ECHO OFF

SET MODE=%1
SET OK=0

IF %MODE%==test (
    docker-compose -f docker/docker-compose-test.yml up --build
    SET OK=1
)

IF %MODE%==live (
    docker-compose -f docker/docker-compose-live.yml up --build -d
    SET OK=1
)

IF %MODE%==stop_live (
    docker-compose -f docker/docker-compose-live.yml down
    SET OK=1
)

IF %OK%==0 (
    ECHO Run this script with one of the following arguments: test, live, stop_live
)
