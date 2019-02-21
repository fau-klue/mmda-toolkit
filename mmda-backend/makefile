all:
	pipenv run python3 manage.py init_db
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
run:
	pipenv run python3 manage.py runserver
docker:
	docker build -t mmda-backend .
clean:
	pipenv clean
