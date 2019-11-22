#!/bin/bash

#When you first turn on the VM, you have to update and upgrade by the following commands
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install libfreetype6-dev

# Install python dependencies
sudo apt-get install python-pip
sudo apt-get install python-dev
sudo pip install numpy==1.8.2
sudo pip install matplotlib==1.3.1
sudo apt-get install curl

#If you already install above libraries, remove or comment the above commands.

# Run python code
sudo python ./main.py

# Done
echo 'Experiment is done. Check your figures in result folder and finish your report'