# Installation Ubuntu 20.04

https://roboticsbackend.com/install-ubuntu-on-raspberry-pi-without-monitor/

## Setup networking
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
          password: prettyflyforawifi
      addresses: [192.168.1.125/24]
      gateway4: 192.168.1.1	
      dhcp4: false
      optional: false
  version: 2
```

Then run
```shell script
sudo netplan --debug apply
```
