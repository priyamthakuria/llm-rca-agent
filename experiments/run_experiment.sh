#!/bin/bash

# Script to run RCA experiments
# Usage: ./run_experiment.sh <config_file>

# if no arguments are passed { $# } -> denotes the number of arguments.
# if number of arguments -eq 0 then " exit 1 " meaning ' do not run '
if [ $# -eq 0 ]; then
    echo "Usage: ./run_experiment.sh <config_file>"
    echo "Example: ./run_experiment.sh configs/exp_zero_shot.yaml"
    exit 1
fi

CONFIG_FILE=$1

# checking if passed config file exist.
# if not, then again resturn ' exit 1 '
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file $CONFIG_FILE not found"
    exit 1
fi

echo "Running experiment with config: $CONFIG_FILE"
python -m src.experiments.runner --config "$CONFIG_FILE"

