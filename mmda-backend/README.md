# MMDA backend

## Installation

    # install pipenv
    pip3 install -r requirements.txt

    # dependency management via pipenv
    pipenv install --dev
    
    # if you run into problems, try installing
    apt-get install python3-dev gcc
    
See also the Dockerfile for a working system environment.


## Settings

Set system parameters in

    backend/settings.py
    
and environment-specific settings (development, testing, production) in

    backend/settings_{ENVIRONMENT}.py


## Database initialisation

    # Create DB tables and populate the roles and users tables
    pipenv run flask --app backend database init


## Running in development

    # Start the Flask development web server
    pipenv run flask --app backend --debug run

You can access the API at http://localhost:5000/.


## Running in production

We use gunicorn 

    # Start the WGSI production web server
    pipenv run gunicorn -w 8 --timeout 600 --bind localhost:5000 wsgi:app

See https://flask.palletsprojects.com/en/2.2.x/deploying/ for further options.


## cURL API Examples

To consume the Flask API you'll first need to login and acquire an [JSON Web Token](https://jwt.io/).

    # Get a JWT Token and export it as TOKEN
    export TOKEN=$(curl -H 'Content-Type: application/json' -X POST http://localhost:5000/api/login/ -d '{"username": "admin", "password": "0000"}' |  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

    # Use the Token
    curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/test-login/
    curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/test-admin/

You can then e.g. create and access discoursemes:

    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json"  -X POST http//localhost:5000/api/user/admin/discourseme/ -d '{"name": "NewDiscourseme", "items": ["new", "discourseme"]}'
    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json" -X GET http://localhost:5000/api/user/admin/discourseme/1/


## Development notes

### Tests

    # Start the Flask development web server
    py.test tests/

    # With coverage
    py.test --cov-report term-missing -v --cov=backend/

### Sphinx documentation

    # Create HTML Documentation
    cd docs/
    make html

### Pylint

    # Running pylint
    pylint --rcfile=.pylintrc backend/*/*.py


## SMTP

Edit the `settings.py` file.

Specifically set all the MAIL_... settings to match your SMTP settings

You can use MailHog as a development server.
See https://github.com/mailhog/MailHog

Note that Google's SMTP server requires the configuration of "less secure apps".
See https://support.google.com/accounts/answer/6010255?hl=en

Note that Yahoo's SMTP server requires the configuration of "Allow apps that use less secure sign in".
See https://help.yahoo.com/kb/SLN27791.html
