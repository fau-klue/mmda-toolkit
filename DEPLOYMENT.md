# MMDA Deployment

The MMDA Demo currently (January 2019) runs on the server *geuselambix.phil.uni-erlangen.de*

For deploying a new version please use the custom shell script provided:

```bash
/root/mmda-deploy.sh
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

The nginx webserver is configured using a custom configuration file (see repository). For extra protection a htpasswd file is provided on the server and then mounted into the Docker Container.

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

