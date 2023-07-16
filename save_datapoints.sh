#!/bin/bash

# chmod +x save_datapoints.sh - before executing --> then sudo ./save_datapoints.sh
read -p "Enter the location : " location
read -p "How many times would you like to save the access points? : " n
count=1

while [ $count -le $n ];
    do
        if sudo python3 -m detect_location.save_data "$location"; then
            echo "Updated new access point"
            ((count++))
            sleep 1
        else
            echo "Execution failed!"
        fi
    done