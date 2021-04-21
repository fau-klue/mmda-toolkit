# Production Installation

1. Install Docker, see https://docs.docker.com/install/

2. Create data directories on the server:

```bash
# Example:
mkdir /opt/data/mmda/database
mkdir /opt/data/mmda/cwb
mkdir /opt/data/mmda/wectors
```

3. Prepare WordVectors:

```bash
# Examples:
cp wordvectors.magnitude /opt/data/mmda/wectors
```

4. Prepare Corpora settings:

```bash
# Examples:
cp mmda-backend/backend/corpora_settings_production.py /opt/data/mmda/
# Add your corpora
vi /opt/data/mmda/corpora_settings_production.py
```

5. Copy systemd unit files

```bash
cp deployment/docker-mmda-backend.service /etc/systemd/system/
cp deployment/docker-mmda-frontend.service /etc/systemd/system/
systemctl reload-daemon
```

6. (optional) Create self-signed TLS certificat if Let's Encrypt is not used:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /opt/data/mmda/cert.key -out /opt/data/mmda/cert.crt
```

7. Adjust systemd unit files to your system:

```bash
vi /etc/systemd/system/docker-mmda-backend.service
 # Change key to random 32 char string
 -e SECRET_KEY=CHANGEME! \
 # Change path to TLS cert and key
 -e TLS_CERTFILE=/certs/letsencrypt/live/geuselambix.phil.uni-erlangen.de/fullchain.pem \
 -e TLS_KEYFILE=/certs/letsencrypt/live/geuselambix.phil.uni-erlangen.de/privkey.pem \
 # Change path to CWB registry
 -v /opt/data/mmda/cwb:/opt/cwb:ro \

vi /etc/systemd/system/docker-mmda-fronend.service
 # Change path to TLS cert and key
 -v /etc/letsencrypt:/certs/letsencrypt:ro \
```

8. Initially the Docker images need to be build manually

```bash
cd mmda-backend
docker build --pull --force-rm -t fau.de/mmda-backend:latest .
cd mmda-frontend
docker build --pull --force-rm -t fau.de/mmda-frontend:latest .
```

9. Enable and start systemd units

```bash
systemctl enable docker-mmda-backend
systemctl start docker-mmda-backend
systemctl enable docker-mmda-frontend
systemctl start docker-mmda-frontend
```

# MMDA Deployment

The MMDA Demo currently (January 2019) runs on the server *geuselambix.phil.uni-erlangen.de*

For deploying a new version please use the custom shell script provided:

```bash
/root/mmda-deploy.sh

# With version (branch or tag):
/root/mmda-deploy.sh branch-name
/root/mmda-deploy.sh tag
```

## Docker

The Application is deployed using Docker Containers.

### Backend Image

The Backend Image is based on the [cwb-ucs Image](https://hub.docker.com/r/martialblog/docker-corpus-tool/) and can be adjusted using Environment Variables (see Dockerfile).

**Build**

```bash
docker build --pull --force-rm -t fau.de/mmda-backend:latest .
```

## Frontend Image

The Frontend uses multilayered build. All dependencies are collected using the [node:alpine Image](https://hub.docker.com/_/node/) and then copied into a production ready [nginx Image](https://hub.docker.com/_/nginx/).

**Build**

```bash
docker build --pull --force-rm -t fau.de/mmda-frontend:latest .
```

The nginx webserver is configured using a custom configuration file (see repository). For extra protection a htpasswd file can be provided on the server and then mounted into the Docker Container.

```bash
# htpasswd location
ls /opt/nginx

# htpasswd format
cat /opt/nginx/htpasswd
mmda:thisisanopensslhash

# htpasswd hash generation
openssl passwd -apr1
```

## Let's Encrypt SSL

SSL encrypttion is provided using Let's Encrypt. For this automated certificates have been created using [certbot](https://hub.docker.com/r/certbot/certbot/).

Hint: You just have to do this when installing the server. Use the provided systemd Timers to automate the renewal.

```bash
docker run -ti --rm -v /etc/letsencrypt:/etc/letsencrypt certbot/certbot certonly --webroot -w /etc/letsencrypt -d geuselambix.phil.uni-erlangen.de
```

Let's Encrypt certificates expire every 90 days for security reasons. Renewal was automated using systemd Timer:

```bash
docker run -t --rm -v /etc/letsencrypt:/etc/letsencrypt certbot/certbot renew --webroot -w /etc/letsencrypt
```

*Hint:* The /etc/letsencrypt directory is mounted into the nginx Container.

## Systemd

Front- and Backend Containers are controlled using systemd. For this custom Service files were written for starting/stopping the Containers. All environment variables and volumes are set here.

```bash
ls /etc/systemd/system/docker-mmda-frontend.service

ls /etc/systemd/system/docker-mmda-backend.service
```

```bash
systemctl start docker-mmda-frontend.service
systemctl stop docker-mmda-frontend.service
systemctl restart docker-mmda-frontend.service
systemctl status docker-mmda-frontend.service

systemctl start docker-mmda-backend.service
systemctl stop docker-mmda-backend.service
systemctl restart docker-mmda-backend.service
systemctl status docker-mmda-backend.service

# Reload after file changes
systemctl daemon-reload
```

## Resources

All resources required for running the application are at */opt*. These get mounted into the Containers

    - /opt/nginx/htpasswd # nginx htpasswd
    - /opt/mmda/corpora.ini # Backend config for available corpora
    - /opt/mmda/wectors # Gensim Word2Vec files
    - /opt/mmda/cwb/data # CWB Corpus Data
    - /opt/mmda/cwb/registry # CWB Registry
    - /opt/mmda/cwb/vrt # Raw Corpus Files for import
