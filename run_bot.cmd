@ECHO OFF

SET MODE=%1

IF "%MODE%"=="test" (
    docker-compose -f docker/docker-compose-test.yml up --build
    GOTO :END
)

IF "%MODE%"=="live" (
    docker-compose -f docker/docker-compose-live.yml up --build -d
    GOTO :END
)

IF "%MODE%"=="stop_live" (
    docker-compose -f docker/docker-compose-live.yml down
    GOTO :END
)

:USAGE
ECHO Run this script with one of the following arguments: test, live, stop_live

:END
