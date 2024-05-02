#!/bin/bash

# Directory to watch
DIRECTORY_TO_WATCH="."

# Command to run
COMMAND="pytest"

# Exclude directories or files
EXCLUDE='(\.pytest_cache|__pycache__|\.pyc|\.log$)|./.venv'

echo "Starting to monitor changes in $DIRECTORY_TO_WATCH for running $COMMAND..."

# Using inotifywait to watch for changes recursively in the specified directory
inotifywait -m -r -e close_write --exclude $EXCLUDE "$DIRECTORY_TO_WATCH" | while read -r directory events filename; do
    clear
    echo "Change detected in $directory$filename. Running $COMMAND..."
    # Run pytest and capture output
    output=$($COMMAND 2>&1)
    exit_code=$?
    echo "$output"
    if [ $exit_code -ne 0 ]; then
        # Display a pop-up if tests fail
        echo "$output" | zenity --text-info --title="Test Failure" --width=500 --height=500
    fi
done
