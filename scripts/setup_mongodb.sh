# Raspberry
sudo apt install -y mongodb
systemctl status mongodb

# in /etc/mongodb.conf comment out bind_ip
# IP address of the server is equal to the device IP
comment bind_ip = 127.0.0.1 # bind_ip = 127.0.0.1
sudo systemctl restart mongodb
sudo systemctl enable mongodb

# setup authentication
mongo
--> use admin
--> db.addUser( { user: "admin", pwd: "root", roles: [ "userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"] } )
--> exit

# in /etc/mongodb.conf uncomment security
auth = true

sudo systemctl restart mongodb

# check to see that auth is enabled
mongo
--> db.adminCommand({listDatabases: 1})
