#!/bin/bash

# set environment variables if this is not being run in docker
if [ -z $TABLO_IP ]; then
    export TABLO_IP=10.0.1.5
fi

if [ -z $DELETE_AFTER_EXPORT ]; then
    export DELETE_AFTER_EXPORT=True
fi

if [ -z $EXEC_INTERVAL_MINUTES ]; then
    export EXEC_INTERVAL_MINUTES=15
fi


while true
do
    ./nfte.py
    sleep "$EXEC_INTERVAL_MINUTES"m
done
