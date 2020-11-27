#!/bin/bash

# create db
mongo
use iot_db
use admin
db.createUser({ user: "admin", pwd: "mongo_admin_iot", roles: [ "userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"] })


sudo nano /etc/mongod.conf
# These two lines must be uncommented and in the file together:
security:
   authorization: enabled
# Change the bindIp to '0.0.0.0':
net:
   port: 27017
   bindIp: 0.0.0.0

sudo systemctl restart mongod
sudo ufw allow 27017/tcp