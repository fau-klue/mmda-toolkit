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


# DEVELOPMENT SERVER
run:
	pipenv run flask --app backend --debug run

run_algorist:
	export CORPUS_REGISTRY='/home/ausgerechnet/corpora/cwb/registry/' &&\
	export CORPORA_SETTINGS='/home/ausgerechnet/corpora/cwb/mmda-corpora.py' &&\
	pipenv run flask --app backend --debug run


# PRODUCTION SERVER
run_obelix:
        export SQL_DATABASE_URI='sqlite:////data/Philipp/mmda/mmda.sqlite' && \
        export CORPORA_SETTINGS='/data/Philipp/mmda/mmda-corpora.py' && \
        export CWB_REGISTRY_PATH='/data/corpora/cqpweb/registry/' &&\
        export ENVIRONMENT='production' &&\
        pipenv run gunicorn -w 16 --certfile=fullchain13.pem --keyfile=privkey13.pem --timeout 3600 --bind :5051 wsgi:app


# DOCKER
docker_build:
	docker build -t mmda-backend .

docker:
	docker run -ti \
	-e WORKERS=8 \
	-e CORPUS_REGISTRY=/app/tests/corpora/registry/ \
	-e CORPORA_SETTINGS=/app/tests/corpora/corpora.py \
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
