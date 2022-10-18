#!/usr/bin/env sh

ENVIRONMENT=${ENVIRONMENT:-'production'}
WORKERS=${WORKERS:-8}

# initialise database (runs idempotently)
echo "Creating Database"
flask --app backend database init

# start server
echo "starting Application ($ENVIRONMENT)"
if [ "$ENVIRONMENT" = 'development' ]; then
    flask --app backend --debug run
else
    python3 wsgi_gevent.py
    # gunicorn -w $WORKERS --timeout 600 --bind :5000 wsgi:app
fi
