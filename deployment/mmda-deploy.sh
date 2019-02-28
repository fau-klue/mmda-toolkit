#!/usr/bin/env sh
# Deployment script for MMDA
# Clones from git, builds and starts the new Docker containers

set -ex

# Clone repo from git
# Deploy Keys are enabled in GitLab
rm -rf /tmp/mmda
git clone git@gitlab.cs.fau.de:efe/mmda-refactor.git /tmp/mmda

# Stop Running Services
# See /etc/systemd/system/docker-mmda-frontend.service
systemctl stop docker-mmda-frontend.service
# See /etc/systemd/system/docker-mmda-backend.service
systemctl stop docker-mmda-backend.service

# Build images
cd /tmp/mmda/mmda-frontend
docker build --pull --force-rm -t fau.de/mmda-frontend:latest .

cd /tmp/mmda/mmda-backend
docker build --pull --force-rm -t fau.de/mmda-backend:latest .

# Cleanup Stale Docker Images
docker image prune -f

# Start Services
systemctl start docker-mmda-backend.service
systemctl start docker-mmda-frontend.service
