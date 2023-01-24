# INSTALL
install:
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

marginals:
	export CORPORA_SETTINGS='/home/ausgerechnet/corpora/cwb/mmda-corpora.py' &&\
	export CWB_REGISTRY_PATH='/home/ausgerechnet/corpora/cwb/registry/' &&\
	pipenv run flask --app backend keyword marginals


# DEVELOPMENT SERVER
run:
	pipenv run flask --app backend --debug run

run_abacist:
	export CORPORA_SETTINGS='/home/ausgerechnet/corpora/cwb/mmda-corpora.py' &&\
	export CWB_REGISTRY_PATH='/home/ausgerechnet/corpora/cwb/registry/' &&\
	pipenv run flask --app backend --debug run


# PRODUCTION SERVER
run_production:
	export ENVIRONMENT='production' &&\
	pipenv run gunicorn -w 8 --timeout 600 --bind localhost:5000 wsgi:app

run_production_gevent:
	export ENVIRONMENT='production' &&\
	pipenv run python wsgi_gevent.py


# DOCKER
docker_build:
	docker build -t mmda-backend .

docker:
	docker run -ti \
	-e WORKERS=8 \
	-e CORPORA_SETTINGS=/app/tests/corpora/corpora.py \
	-e CWB_REGISTRY_PATH=/app/tests/corpora/registry/ \
	-e SQL_DATABASE_URI=sqlite:////opt/mmda.sqlite \
	-p 5000:5000 \
	--name mmda-backend \
	mmda-backend

docker_abacist:
	docker run -ti \
	-v /home/ausgerechnet/implementation/mmda-toolkit/mmda-backend/instance/:/opt/mmda/ \
	-v /home/ausgerechnet/corpora/cwb/mmda-corpora.py:/opt/mmda-corpora.py:ro \
	-v /home/ausgerechnet/corpora/cwb/registry/:/opt/cwb/registry/:ro \
	-v /home/ausgerechnet/corpora/cwb/data/:/home/ausgerechnet/corpora/cwb/data/:ro \
	-v /home/ausgerechnet/corpora/embeddings/magnitude/:/home/ausgerechnet/corpora/embeddings/magnitude/:ro \
	-e WORKERS=8 \
	-p 5000:5000 \
	--name mmda-backend \
	 mmda-backend

docker_obelix:
	docker run \
	-v /data/Philipp/mmda/:/opt/mmda/ \
	-v /data/Philipp/mmda/mmda-corpora.py:/opt/mmda-corpora.py:ro \
	-v /data/corpora/cqpweb/registry/:/opt/cwb/registry/:ro \
	-v /data/corpora/cqpweb/corpora/:/data/corpora/cqpweb/corpora/:ro \
	-v /cip/corpora/projects/EFE/embeddings/:/opt/embeddings/:ro \
	-v /etc/letsencrypt/:/certs/letsencrypt/:ro \
	-e TLS_ENABLE=true \
	-e TLS_CERTFILE=/certs/letsencrypt/live/corpora.linguistik.uni-erlangen.de/fullchain.pem \
	-e TLS_KEYFILE=/certs/letsencrypt/live/corpora.linguistik.uni-erlangen.de/privkey.pem \
	-e ENVIRONMENT=production \
	-e SECRET_KEY=fLVmrrpwjjHfdshvsrewqlbpuvcsewhrsdfweh \
	-e WORKERS=16 \
	-p 5000:5000 \
	--name mmda-backend \
	mmda-backend
