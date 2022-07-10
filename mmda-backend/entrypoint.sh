#!/usr/bin/env sh
# Entrypoint for Docker


ENVIRONMENT=${ENVIRONMENT:-'production'}
WORKERS=${WORKERS:-4}


# Initialize database (runs idempotently) and run migrations.
# echo "Running Database Migrations"
# python3 manage.py migrate_db upgrade
echo "Creating Database"
python3 manage.py init_db

# Start the WSGI production server
echo "Starting Application ($ENVIRONMENT)"

if [ "$ENVIRONMENT" = 'development' ]; then
    python3 manage.py runserver
else
    gunicorn -w $WORKERS --timeout 600 --bind :5000 backend.commands.wsgi:app
fi
