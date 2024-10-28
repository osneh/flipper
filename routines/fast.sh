#!/bin/bash

# Check if at least one parameter is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <parameter>"
  exit 1
fi

# Store the first parameter
PARAMETER=$1

source delete.sh
##echo $PARAMETER
source RUNtcp.bat $PARAMETER 
