# Installation Ubuntu 20.04

Follow the [Installation manual](https://roboticsbackend.com/install-ubuntu-on-raspberry-pi-without-monitor/ "Installation manual") to install Ubuntu20.04 in headless mode for Raspberry pir/

## System setup
Create a new root user
```
sudo adduser dankers-iot
sudo usermod -aG sudo dankers-iot
```

## Setup networking

Change firewall settings to allow for ssh traffic.
```
sudo ufw allow ssh
```

Set a fixed IP for ETH0

todo!! 

Add the following to ``` /etc/netplan/00-installer-config.yaml ```
```
network:
  ethernets:
    eth0:
      addresses: [10.42.0.25/24]
      gateway4: 10.42.0.10
      nameservers:
        addresses: [4.2.2.2, 8.8.8.8]
  wifis:
    wlan0:
      access-points:
        SaveOurWinters:
          password: "prettyflyforawifi"
      addresses: [192.168.1.125/24]
      gateway4: 192.168.1.1	
      dhcp4: false
      optional: false
  version: 2
```

## MQTT broker
Intall Mosquitto 

## MongoDB
Install Mongodb



Then run
```shell script
sudo netplan --debug apply
```
