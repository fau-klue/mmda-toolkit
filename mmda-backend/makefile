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
run_production_gevent:
	export ENVIRONMENT='production' &&\
	pipenv run python wsgi_gevent.py

run_production:
	export ENVIRONMENT='production' &&\
	pipenv run gunicorn -w 8 --timeout 600 --bind localhost:5000 wsgi:app


# DOCKER
docker_build:
	docker build -t mmda-backend .

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
	mmda-backend
