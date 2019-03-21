# MMDA Backend

# Setup

## Install Dependencies

    # Init pyvenv
    python3 -m venv && source .venv/bin/activate

    # Install Pipenv
    pip3 install -r requirements.txt

    # Install dependencies
    pipenv install

## Create local settings

    # Copy the examples to adjust the settings
    cp backend/corpora_settings_example.py backend/corpora_settings_development.py
    cp backend/local_settings_example.py backend/local_settings_development.py

## Initializing the Database

    # Create DB tables and populate the roles and users tables
    python manage.py init_db

    # Run the migrations
    python manage.py migrate

## Running the app (development)

    # Start the Flask development web server
    python manage.py runserver

Point your web browser to http://localhost:5000/

## Configuring SMTP

Edit the `local_settings_development.py` file.

Specifically set all the MAIL_... settings to match your SMTP settings

You can use MailHog as a development server.
See https://github.com/mailhog/MailHog

Note that Google's SMTP server requires the configuration of "less secure apps".
See https://support.google.com/accounts/answer/6010255?hl=en

Note that Yahoo's SMTP server requires the configuration of "Allow apps that use less secure sign in".
See https://help.yahoo.com/kb/SLN27791.html


# Development

## Sphinx Documentation

    # Create HTML Documentation
    cd docs/
    make html

## Running pylint

    # Running pylint
    pylint --rcfile=.pylintrc backend/*/*.py

## Running the automated tests

    # Start the Flask development web server
    py.test tests/

    # With coverage
    py.test --cov-report term-missing -v --cov=backend/


# Deployment

# Running in production

    # Start the wGSI production web server
    python manage.py run_wsgi

See http://flask.pocoo.org/docs/1.0/deploying/

# cUrl Examples

Here are some examples on how to use the API.

To consume the Flask API you'll first need to login and acquire an [JSON Web Token](https://jwt.io/).

## JWT Token

    # Get a JWT Token
    curl -v -H "Content-type: application/json" -X POST http://localhost:5000/api/login/ -d '{"username": "admin", "password": "Squanchy1"}
    curl -v -H "Content-type: application/json" -X POST http://localhost:5000/api/login/ -d '{"username": "student1", "password": "Erlangen1"}

    # Save the Token in an ENV variable
    export TOKEN='<THE TOKEN>'

    # Onelines
    export TOKEN=$(curl -H 'Content-Type: application/json' -X POST http://localhost:5000/api/login/ -d '{"username": "admin", "password": "Squanchy1"}' |  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    export TOKEN=$(curl -H 'Content-Type: application/json' -X POST http://localhost:5000/api/login/ -d '{"username": "student1", "password": "Erlangen1"}' |  python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

    # Use the Token
    curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/test-login/
    curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/test-admin/


## Create Analysis

    # Add Analysis
    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json" -X POST http://localhost:5000/api/user/student1/analysis/ -d '{"name": "foobar", "items": ["Merkel","Atom"]}'

    # Delete Analysis
    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json" -X DELETE http://localhost:5000/api/user/student1/analysis/1/


## Create Discourseme

    # Add new Discourseme
    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json" -X POST http://localhost:5000/api/user/student1/discourseme/ -d '{"name": "foobar", "items": ["hans"]}'

    # Add Discourseme to Analysis
    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json" -X PUT http://localhost:5000/api/user/student1/analysis/1/discourseme/2/

    # Remove Discourseme from  Analysis
    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json" -X DELETE http://localhost:5000/api/user/student1/analysis/1/discourseme/2/

## Get Corpora

    # Get all corpora
    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json" -X GET http://localhost:5000/api/corpus/

    # Get corpus
    curl -v -H "Authorization: Bearer $TOKEN" -H "Content-type: application/json" -X GET http://localhost:5000/api/corpus/FAZ_SMALL


