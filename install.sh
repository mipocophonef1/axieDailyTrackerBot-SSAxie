#!/bin/bash
homedir=/home/ubuntu
apppath="axieDailyTrackerBot-SSAxie"
echo "Installing the requirements ... "

#appending source list required for the application 
sudo echo "deb http://archive.ubuntu.com/ubuntu bionic main universe" >> /etc/apt/sources.list
sudo echo "deb http://archive.ubuntu.com/ubuntu bionic-security main universe" >> /etc/apt/sources.list
sudo echo "deb http://archive.ubuntu.com/ubuntu bionic-updates main universe" >> /etc/apt/sources.list

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
