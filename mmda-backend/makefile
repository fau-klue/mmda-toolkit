.PHONY: discoursemes

# INSTALL
install:
	pip3 install -r requirements.txt
	pipenv install --dev


# TEST
lint:
	pipenv run pylint --rcfile=.pylintrc backend/*/*.py

test:
	pipenv run pytest -v

coverage:
	pipenv run pytest --cov-report term-missing -v --cov=backend/


# DATABASE
new_database: clear_db database discoursemes

database:
	pipenv run python3 manage.py init_db

discoursemes:
	pipenv run python3 discoursemes/init-discoursemes.py

migrate:
	pipenv run python3 manage.py migrate_db upgrade


# RUN DEVELOPMENT SERVER
run:
	pipenv run python3 manage.py runserver

windowed:
	database
	gnome-terminal -- pipenv run python3 manage.py runserver

rerun_force: clear_all install database run


# DOCKER (CONTAINERED PRODUCTION SERVER)
docker: docker_clean docker_run

docker_build:
	docker build -t mmda-backend .

docker_run:
	docker run -ti \
	-v /data/Philipp/mmda/:/opt/database/ \
	-v /data/Philipp/mmda/corpora_settings_production.py:/app/backend/corpora_settings_production.py:ro \
	-v /cip/corpora/projects/EFE/embeddings/:/opt/embeddings/:ro \
	-v /data/corpora/cqpweb/registry/:/opt/cwb/registry/:ro \
	-v /data/corpora/cqpweb/corpora/:/data/corpora/cqpweb/corpora/:ro \
	-v /etc/letsencrypt/:/certs/letsencrypt/:ro \
	-e TLS_ENABLE=true \
	-e TLS_CERTFILE=/certs/letsencrypt/live/corpora.linguistik.uni-erlangen.de/fullchain.pem \
	-e TLS_KEYFILE=/certs/letsencrypt/live/corpora.linguistik.uni-erlangen.de/privkey.pem \
	-e CWB_REGISTRY_PATH=/opt/cwb/registry/ \
	-e SQL_DATABASE_URI=sqlite:////opt/database/mmda.sqlite \
	-e SECRET_KEY=SFDVwejisadxslkhewq!$sadvxdflfw23$!Rwcd9§ \
	-p 5000:5000 \
	--name mmda-backend \
	mmda-backend

docker_clean:
	docker container rm mmda-backend

docker_stop:
	docker container stop mmda-backend


# CLEAN LOCAL STUFF
clear_all: clear_cache clear_db clear_lock

clear_cache:
	rm instance/ccc-cache -r
	rm /tmp/mmda-anycache -r

clear_db:
	rm instance/mmda.sqlite

clear_lock:
	rm Pipfile.lock
