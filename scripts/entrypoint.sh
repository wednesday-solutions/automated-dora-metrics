#!/bin/bash

if [ "$1" = "--notify-compass" ]; then
    shift
    "./scripts/notify-compass.sh" "$@"
elif [ "$1" = "--calculate-metrics" ]; then
    shift
    python "./automation.py" "$@"
else
    echo "No valid option specified. Exiting."
fi
