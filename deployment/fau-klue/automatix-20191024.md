# install docker

## prerequisites
sudo apt update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88

## add repo
sudo echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable" > /etc/apt/sources.list.d/docker.list

## install
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# clone repository
git clone git@gitlab.cs.fau.de:efe/mmda-refactor.git
cd mmda-refactor/mmda-backend/deployment

# change files
sudo cp docker-mmda-*.service /etc/systemd/system/
sudo systemctl daemon-reload

change `secret_key` in /etc/systemd/system/docker-mmda-backend.service
set `tls_enable` to false

sudo mkdir -p /opt/data/mmda/{cwb,database,wectors}


# create images
cd ../mmda-backend
sudo docker build --pull --force-rm -t fau.de/mmda-backend:latest .

cd ../mmda-frontend
sudo docker build --pull --force-rm -t fau.de/mmda-frontend:latest .

# Stop Services
systemctl stop docker-mmda-frontend.service
systemctl stop docker-mmda-backend.service

# Start Services
systemctl start docker-mmda-backend.service
systemctl start docker-mmda-frontend.service

# Cleanup Stale Docker Images
docker image prune -f
