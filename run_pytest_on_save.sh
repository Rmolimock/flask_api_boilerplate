#!/bin/bash

# Directory to watch
DIRECTORY_TO_WATCH="."

# Command to run
COMMAND="pytest"

# Exclude directories or files
EXCLUDE='(\.pytest_cache|__pycache__|\.pyc|\.log$)'

echo "Starting to monitor changes in $DIRECTORY_TO_WATCH for running $COMMAND..."

# Using inotifywait to watch for changes recursively in the specified directory
# -m: Monitor mode (keeps inotifywait running after initial events are received)
# -r: Recursive mode (watches subdirectories)
# --exclude: Exclude events on files matching the regular expression
inotifywait -m -r -e close_write --exclude $EXCLUDE "$DIRECTORY_TO_WATCH" | while read -r directory events filename; do
    echo "Change detected in $directory$filename. Running $COMMAND..."
    $COMMAND
done
