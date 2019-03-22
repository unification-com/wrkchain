#!/bin/bash
set -e

# If "-e uid={custom/local user id}" flag is not set for "docker run" command, use 9999 as default
CURRENT_UID=${HOST_UID:-9999}

# Notify user about the UID selected
echo "Current UID : $CURRENT_UID"
# Set "HOME" ENV variable for user's home directory
export HOME=/home/sdkuser

export PATH="/home/sdkuser/.pyenv/versions/3.7.2/bin:${PATH}"
export PYTHONPATH=/home/sdkuser/sdk

# Execute process
exec /usr/local/bin/gosu sdkuser "$@"