#!/bin/bash
set -e

CURRENT_UID=${HOST_UID:-9999}

# Notify user about the UID selected
echo "Current UID : $CURRENT_UID"
echo "Host build DIR : $HOST_BUILD_DIR"
# Set "HOME" ENV variable for user's home directory
export HOME=/home/sdkuser

export PATH="/home/sdkuser/.pyenv/versions/3.7.2/bin:${PATH}"
export PYTHONPATH=/home/sdkuser/sdk

# Evaluate environment variables
exec /usr/local/bin/gosu sdkuser $(eval echo "$@")

# Execute process
exec /usr/local/bin/gosu sdkuser "$@"