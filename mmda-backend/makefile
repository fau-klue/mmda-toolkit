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
	pipenv run flask --app backend database init


# DEVELOPMENT SERVER
run:
	pipenv run flask --app backend --debug run


# PRODUCTION SERVER
production:
	pipenv run gunicorn -w 4 --timeout 600 --bind localhost:5000 wsgi:app


# PRODUCTION SERVER VIA DOCKER (on abacist)
docker: docker_clean docker_run_abacist

docker_build:
	docker build -t mmda-backend .

docker_clean:
	docker container rm mmda-backend

docker_stop:
	docker container stop mmda-backend

docker_run_abacist:
	docker run -ti \
	-v /home/ausgerechnet/implementation/mmda-toolkit/mmda-backend/instance/:/opt/database/ \
	-v /home/ausgerechnet/implementation/mmda-toolkit/mmda-backend/backend/settings_production.py:/app/backend/settings_production.py:ro \
	-v /home/ausgerechnet/corpora/embeddings/magnitude/:/opt/embeddings/:ro \
	-v /home/ausgerechnet/corpora/cwb/registry/:/opt/cwb/registry/:ro \
	-v /home/ausgerechnet/corpora/cwb/data/:/home/ausgerechnet/corpora/cwb/data/:ro \
	-e SECRET_KEY=SFDVwejisadxslkhewq!$sadvxdflfw23$!Rwcd9§ \
	-e WORKERS=8 \
	-p 5000:5000 \
	--name mmda-backend \
	mmda-backend


# CLEAN LOCAL STUFF
clean: clean_cache clean_db

clean_cache:
	rm -r instance/ccc-data*
	rm -r /tmp/mmda-anycache

clean_db:
	rm instance/mmda*.sqlite
