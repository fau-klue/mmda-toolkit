all:
	gnome-terminal -- npm run serve
	code .
	firefox localhost:8080 &
install:
	npm install yarn
	yarn install || npm install
lint:
	yarn run lint || npm run lint
test:
	yarn run 'test:unit' || npm run 'test:unit'
run:
	yarn run serve || npm run serve
build:
	yarn run build || npm run build
clean:
	rm -rf node_modules/
docker_build:
	docker build -t mmda-frontend .
docker_run:
	docker run -ti \
	 --net bridge -m 0b --link mmda-backend \
	 -v /opt/data/nginx/htpasswd:/etc/nginx/.htpasswd:ro \
	 -v /etc/letsencrypt:/certs/letsencrypt:ro \
	 -p 80:80 \
	 -p 443:443 \
	--name mmda-frontend \
	mmda-frontend
