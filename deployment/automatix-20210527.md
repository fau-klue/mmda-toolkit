# install docker
see https://docs.docker.com/engine/install/ubuntu/

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
