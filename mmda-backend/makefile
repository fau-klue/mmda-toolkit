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
database:
	pipenv run python3 manage.py init_db

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
	docker run -ti --name mmda-backend \
	-v /home/ausgerechnet/corpora/mmda/:/opt/database/ \
	-v /home/ausgerechnet/corpora/embeddings/magnitude/:/opt/embeddings/ \
	-v /home/ausgerechnet/corpora/cwb/registry/:/opt/cwb/registry/:ro \
	-v /home/ausgerechnet/corpora/cwb/data/:/home/ausgerechnet/corpora/cwb/data/:ro \
	-e CWB_REGISTRY_PATH=/opt/cwb/registry/ \
	-e SQL_DATABASE_URI=sqlite:////opt/database/mmda.sqlite \
	-p 5000:5000 \
	mmda-backend

docker_clean:
	docker container rm mmda-backend

docker_stop:
	docker container stop mmda-backend


# CLEAN LOCAL STUFF
clear_all: clear_cache clear_db clear_lock

clear_cache:
	rm /tmp/mmda-ccc/ -r
	rm /tmp/mmda-anycache/ -r

clear_db:
	rm /tmp/mmda.sqlite

clear_lock:
	rm Pipfile.lock
