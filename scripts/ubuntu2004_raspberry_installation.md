# Installation Ubuntu 20.04 server

Follow the [Installation manual](https://roboticsbackend.com/install-ubuntu-on-raspberry-pi-without-monitor/ "Installation manual") to install Ubuntu20.04 in headless mode for Raspberry pir/

## System setup
Create a new root user
```
sudo adduser dankers-iot
sudo usermod -aG sudo dankers-iot
```
Remove automatic updates
```
sudo apt remove unattended-upgrades
```


## Setup networking

Change firewall settings to allow for ssh traffic.
```
sudo ufw allow ssh
```

todo: Set a fixed IP for ETH0


## MQTT broker
Install Mosquitto 

```
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
