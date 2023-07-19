#!/bin/bash

# create virtual environment
python3 -m venv venv

# activate virtual environment
source venv/bin/activate

# install packages from requirements.txt
pip install -r requirements.txt

# print message
echo "The virtual environment has been set up and packages have been installed."
echo "You are currently in the virtual environment. To exit, run the 'deactivate' command."
