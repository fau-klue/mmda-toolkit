# Production Installation

## build 

- backend

```bash
cd mmda-backend
docker build --pull --force-rm -t fau.de/mmda-backend:latest .
```

- frontend

```bash
cd mmda-frontend
yarn run build || npm run build
```

## resources

- create data directories on the server:

```bash
# Example:
mkdir /opt/data/mmda/database
mkdir /opt/data/mmda/embeddings
```

- import embeddings:

```bash
# Examples:
cp wordvectors.magnitude /opt/data/mmda/embeddings
```

- import settings:

```bash
# Examples:
cp mmda-backend/backend/settings_production.py /opt/data/mmda/
# Add your corpora
vi /opt/data/mmda/settings_production.py
```

## Dockerized backend managed by systemd

- (optional) create self-signed TLS certificat if Let's Encrypt is not used:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /opt/data/mmda/cert.key -out /opt/data/mmda/cert.crt
```

- copy systemd unit files

```bash
cp deployment/docker-mmda-backend.service /etc/systemd/system/
cp deployment/docker-mmda-frontend.service /etc/systemd/system/
systemctl reload-daemon
```

- adjust to your system:

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

- enable and start

```bash
systemctl enable docker-mmda-backend
systemctl start docker-mmda-backend
systemctl enable docker-mmda-frontend
systemctl start docker-mmda-frontend
```

## frontend

- copy dist

        cd /data/corpora/htdocs/
        mkdir mmda
        chgrp www-data mmda
        cp -r dist/* /data/corpora/htdocs/mmda/.

- set up Apache

        ## MMDA
        <Directory /data/corpora/htdocs/mmda/>
                Options Indexes FollowSymLinks MultiViews
                AllowOverride None
                Require all granted
        </Directory>
  
  
