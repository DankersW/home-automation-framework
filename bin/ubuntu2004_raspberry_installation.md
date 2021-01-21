# Installation Ubuntu 20.04 server

Follow the [Installation manual](https://roboticsbackend.com/install-ubuntu-on-raspberry-pi-without-monitor/ "Installation manual") to install Ubuntu20.04 in headless mode for Raspberry pir/

## System setup
Create a new root user
```shell script
sudo adduser dankers-iot
sudo usermod -aG sudo dankers-iot
```
Remove automatic updates
```shell script
sudo apt remove unattended-upgrades
```

## Setup networking

Change firewall settings to allow for ssh traffic.
```shell script
sudo ufw allow ssh
```

fixed IP for ETH0
```shell script
sudo nano /etc/netplan/99_config.yaml
# add to file
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses:
        - 10.42.0.25/24
      gateway4: 10.42.0.10

sudo netplan apply
```

## MQTT broker
Install Mosquitto 

```shell script
sudo apt install mosquitto mosquitto-clients
sudo ufw allow 8883
sudo ufw allow 1883
```

## MongoDB
Install Mongodb
```shell script
curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt update
sudo apt install mongodb-org
sudo systemctl start mongod.service
sudo systemctl status mongod
sudo systemctl enable mongod
mongo --eval 'db.runCommand({ connectionStatus: 1 })'
```

## Temperature
```shell script
sudo apt-get install lm-sensors
sudo sensors-detect
sudo service kmod start
sensors
```
