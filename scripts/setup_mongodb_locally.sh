# Installation Ubuntu2004 on WSL2
# https://derplime.dev/2020/05/31/configuring-wsl-ubuntu-20-04-for-mern-stack-local-development/
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo nano /etc/init.d/mongod
sudo chmod +x /etc/init.d/mongod

sudo service mongod start

# On every re-start of wsl do mongo
mongo


# Trouble shooting
## fix the GPG error “NO_PUBKEY”?
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys <PUBLIC KEY --- E.Q.4B7C549A058F8B6B>
sudo apt-get update