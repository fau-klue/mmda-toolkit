#!/usr/bin/env sh

ENVIRONMENT=${ENVIRONMENT:-'production'}
WORKERS=${WORKERS:-16}
TIMEOUT=${TIMEOUT:-3600}

# initialise database (runs idempotently)
echo "creating database"
flask --app backend database init

# start server
echo "starting application (environment: $ENVIRONMENT)"
if [ "$ENVIRONMENT" = 'development' ]; then
    flask --app backend --debug run
else
    gunicorn -w $WORKERS --certfile=$TLS_CERTFILE --keyfile=$TLS_KEYFILE --timeout $TIMEOUT --bind :5000 wsgi:app
fi
