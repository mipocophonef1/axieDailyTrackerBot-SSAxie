#!/bin/bash
homedir=/home/ubuntu
apppath="axieDailyTrackerBot-SSAxie"
echo "Installing the requirements ... "


echo "Updating source lists"
sudo apt update

echo "Installing python "
sudo apt install -y python3-pip

echo "Updating requirements file"
cd $homedir/$apppath
pip freeze > requirements.txt

echo "Installing application requirements"
pip3 install -r requirements.txt
pip3 install discord
pip3 install web3
pip3 install pyyaml

sudo chown -R ubuntu:ubuntu $homedir/$apppath
