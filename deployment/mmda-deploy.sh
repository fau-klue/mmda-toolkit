#!/usr/bin/env sh
# Deployment script for MMDA
# Clones from git, builds and starts the new Docker containers

set -ex

if [ $# -eq 0 ]
  then
      echo 'INFO: No git reference passed. Using master.'
      echo 'Example: mmda-deploy.sh v1.0.3'
      VERSION='master'
else
    VERSION=$1
fi

# Clone repo from git
# Deploy Keys are enabled in GitLab
rm -rf /tmp/mmda
git clone git@gitlab.cs.fau.de:efe/mmda-refactor.git /tmp/mmda

# Checkout version
cd /tmp/mmda/
git checkout $VERSION

# Build images
cd /tmp/mmda/mmda-frontend
docker build --pull --force-rm -t fau.de/mmda-frontend:latest .

cd /tmp/mmda/mmda-backend
docker build --pull --force-rm -t fau.de/mmda-backend:latest .

# Stop Running Services
# See /etc/systemd/system/docker-mmda-*.service
systemctl stop docker-mmda-frontend.service
systemctl stop docker-mmda-backend.service

# Start Services
systemctl start docker-mmda-backend.service
systemctl start docker-mmda-frontend.service

# Cleanup Stale Docker Images
docker image prune -f
