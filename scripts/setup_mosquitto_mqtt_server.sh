#!/bin/bash

# Install and verify Mosquitto is working on WSL
sudo apt-get install -y mosquitto
service mosquitto status

# Update conf file
echo "persistence false" > /etc/mosquitto/conf.d/myconfig.conf
echo "" > /etc/mosquitto/conf.d/myconfig.conf
echo "listener 1883" > /etc/mosquitto/conf.d/myconfig.conf
echo "protocol mqtt" > /etc/mosquitto/conf.d/myconfig.conf
echo "" > /etc/mosquitto/conf.d/myconfig.conf
sudo service mosquitto restart
service mosquitto status

sudo service mosquitto start
sudo service mosquitto stop
