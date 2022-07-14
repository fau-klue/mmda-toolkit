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
