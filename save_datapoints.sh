#!/bin/bash

# chmod +x save_datapoints.sh - before executing --> then sudo ./save_datapoints.sh
read -p "Enter the location : " location
read -p "How many times would you like to save the access points? : " n
read -p "Do you want to train the model after saving the access points? 1 - Yes, 2 - No: " y

count=1
yes_or_no=$((y))

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

if [ $yes_or_no -eq 1 ]; then
    sudo python3 -m detect_location.train_model
    echo "Successfully trained the model!"
fi