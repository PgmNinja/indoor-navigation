#!/bin/bash

# Prompt the user for the number of times to execute the Python script
# chmod +x save_datapoints.sh - before executing --> then sudo ./save_datapoints.sh
read -p "Enter the location : " location
read -p "How many times would you like to save the access pounts? : " n

# Loop to execute the Python script n times
for ((i=1; i<=$n; i++))
do
    sudo python save_data.py "$location"
    sleep 1
done