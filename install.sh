#!/bin/sh
sudo apt install python3.5-dev
sudo apt install python3-setuptools
sudo apt install wget
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.5 get-pip.py
sudo apt-get install libffi-dev
sudo python3.5 -m pip install -U discord.py[voice]

