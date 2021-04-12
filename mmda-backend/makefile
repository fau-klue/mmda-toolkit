all: database run

windowed: database
	gnome-terminal -- pipenv run python3 manage.py runserver
install:
	pip3 install -r requirements.txt
	pipenv install --dev
lint:
	pipenv run pylint --rcfile=.pylintrc backend/*/*.py
test:
	pipenv run pytest -v
coverage:
	pipenv run pytest --cov-report term-missing -v --cov=backend/
database:
	pipenv run python3 manage.py init_db
db:
	pipenv run python3 manage.py db
run:
	pipenv run python3 manage.py runserver
docker:
	docker build -t mmda-backend .
clean:
	pipenv clean

rerun_force: clear_all install database run

clear_all: clean clear_cache clear_db clear_lock

clear_lock:
	rm Pipfile.lock
clear_cache:
	rm /tmp/mmda-ccc-data/ -r
clear_db:
	rm /tmp/backend.sqlite
