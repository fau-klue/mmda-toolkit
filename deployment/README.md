# Production Installation

## Backend

The backend is deployed using a Docker container.

### build

```bash
cd mmda-backend
docker build -t mmda-backend:latest .
```

### resources

You'll need

- corpora accessible in a CWB registry,
- embeddings in pymagnitude format,
- a Python file with corpus settings,
- a place to store an sqlite database, and
- TLS certificates / key files.

### systemd files

Adjust the [example systemd file](obelix-mmda-backend.service) to your system linking above resources.

Copy the file to /etc/systemd/system/ and start the daemon:

```bash
sudo cp mmda-backend.service /etc/systemd/system/mmda-backend.service
sudo systemctl enable mmda-backend
sudo systemctl reload-daemon
sudo systemctl start mmda-backend.service
```

## Frontend

The frontend is a static build:

    cd mmda-frontend
    yarn run build || npm run build

Copy dist to appropriate place:

    sudo mkdir /data/corpora/htdocs/mmda
    sudo chgrp /data/corpora/htdocs/www-data mmda
    cp -r dist/* /data/corpora/htdocs/mmda/.

Set up Apache:

    ## MMDA
    <Directory /data/corpora/htdocs/mmda/>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride None
        Require all granted
    </Directory>
