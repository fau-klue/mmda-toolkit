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


# DEVELOPMENT SERVER
run:
	pipenv run python3 manage.py runserver


# PRODUCTION SERVER
run_production:
	pipenv run gunicorn -w 2 --timeout 600 --bind localhost:5000 backend.commands.wsgi:app


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
	-v /home/ausgerechnet/implementation/mmda-refactor/mmda-backend/instance/:/opt/database/ \
	-v /home/ausgerechnet/implementation/mmda-refactor/mmda-backend/backend/settings_production.py:/app/backend/settings_production.py:ro \
	-v /home/ausgerechnet/corpora/embeddings/magnitude/:/opt/embeddings/:ro \
	-v /home/ausgerechnet/corpora/cwb/registry/:/opt/cwb/registry/:ro \
	-v /home/ausgerechnet/corpora/cwb/data/:/home/ausgerechnet/corpora/cwb/data/:ro \
	-e SECRET_KEY=SFDVwejisadxslkhewq!$sadvxdflfw23$!Rwcd9§ \
	-e WORKERS=2 \
	-p 5000:5000 \
	--name mmda-backend \
	mmda-backend


# CLEAN LOCAL STUFF
clean: clean_cache clean_db clean_lock

clean_cache:
	rm -r instance/ccc-data*
	rm -r /tmp/mmda-anycache

clean_db:
	rm instance/mmda*.sqlite

clean_lock:
	rm Pipfile.lock
