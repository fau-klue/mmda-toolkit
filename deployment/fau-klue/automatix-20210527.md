# install docker
see https://docs.docker.com/engine/install/ubuntu/

# clone repository
git clone git@gitlab.cs.fau.de:efe/mmda-refactor.git
cd mmda-refactor/mmda-backend/deployment

# system daemon files
sudo cp docker-mmda-*.service /etc/systemd/system/

change /etc/systemd/system/docker-mmda-backend.service
set `secret_key` to NEWPASSWORD
set `tls_enable` to false

sudo systemctl daemon-reload

# resources
sudo mkdir -p /opt/data/mmda/{cwb,database,embeddings,cache}

# create images
cd ../mmda-backend
sudo docker build --pull --force-rm -t fau.de/mmda-backend:latest .

cd ../mmda-frontend
sudo docker build --pull --force-rm -t fau.de/mmda-frontend:latest .

docker image prune -f

# Stop Services
systemctl stop docker-mmda-backend.service
systemctl stop docker-mmda-frontend.service

# Start Services
systemctl start docker-mmda-backend.service
systemctl start docker-mmda-frontend.service

