# MMDA backend

## Installation

See the [Dockerfile](Dockerfile) for a working system environment ready for production.

During development, we use [pipenv](https://github.com/pypa/pipenv) for dependency management.

    pip3 install -r requirements.txt
    pipenv install --dev


## Settings

Default settings are defined in

    settings.py
    
Overwrite your local settings via environment variables:

    - ENVIRONMENT
    - SECRET_KEY
    - SQL_DATABASE_URI
    - CORPORA_SETTINGS
    - CWB_REGISTRY_PATH
    - TLS_ENABLE
    - TLS_CERTFLE
    - TLS_KEYFILE


## Database initialisation

    pipenv run flask --app backend database init


## Running in development

    pipenv run flask --app backend --debug run

You can access the API at http://localhost:5000/.


## Running in production

We use gunicorn 

    export ENVIRONMENT='production' &&\
    pipenv run gunicorn -w 8 --timeout 600 --bind localhost:5000 wsgi:app

See https://flask.palletsprojects.com/en/2.2.x/deploying/ for further options.


## cURL API Examples

To consume the Flask API you'll first need to login and acquire an [JSON Web Token](https://jwt.io/).

    export TOKEN=$(curl -H 'Content-Type: application/json' -X POST http://localhost:5000/api/login/ -d '{"username": "admin", "password": "mmda-admin"}' |  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")


Test login:

    curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/test-login/
    curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/test-admin/

You can then e.g. create and access discoursemes:

    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json"  -X POST http//localhost:5000/api/user/admin/discourseme/ -d '{"name": "NewDiscourseme", "items": ["new", "discourseme"]}'
    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json" -X GET http://localhost:5000/api/user/admin/discourseme/1/


## Development notes

### Tests

    pipenv run pytest -v

### Coverage

    pipenv run pytest --cov-report term-missing -v --cov=backend/

### Pylint

    pipenv run pylint --rcfile=.pylintrc backend/*/*.py

### Sphinx documentation

    cd docs/ && make html && ..
