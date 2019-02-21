all:
	gnome-terminal -- npm run serve
	code .
	firefox localhost:8080 &
install:
	npm install yarn
	yarn install
lint:
	yarn run lint
test:
	yarn run 'test:unit'
run:
	yarn run serve
build:
	yarn run build
clean:
	rm -rf node_modules/
