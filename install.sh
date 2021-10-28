#!/bin/bash
homedir=/home/ubuntu
apppath="axieDailyTrackerBot-SSAxie"

sudo apt update
sudo apt install -y python3-pip

cd $homedir/$apppath
pip freeze > requirements.txt

pip3 install -r requirements.txt
pip3 install discord
pip3 install web3
pip3 install pyyaml

sudo chown -R ubuntu:ubuntu $homedir/$apppath
