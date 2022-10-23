# backend

## build docker container
    
    cd mmda-backend
    make docker_build

## configure and start system daemon

    sudo cp obelix-mmda-backend.service /etc/systemd/system/mmda-backend.service
    sudo systemctl stop mmda-backend.service
    sudo systemctl start mmda-backend.service

## test

    export TOKEN=$(curl -H 'Content-Type: application/json' https://corpora.linguistik.uni-erlangen.de:5000/api/login/ -d '{"username": "admin", "password": "mmda-admin"}' |  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json" https://corpora.linguistik.uni-erlangen.de:5000/api/user/admin/discourseme/ -d '{"name": "TestTesterson", "items": ["COVID-19"]}'


# frontend

## prepare destination

    cd /data/corpora/htdocs/
    sudo mkdir mmda
    sudo chown snphhein mmda
    sudo chgrp www-data mmda

## build & deploy

    cd mmda-frontend
    make build
    scp -r dist/* obelix:/data/corpora/htdocs/mmda/.
