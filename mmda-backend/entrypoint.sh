#!/usr/bin/env sh
# Entrypoint for Docker


ENVIRONMENT=${ENVIRONMENT:-'development'}


# Initialize database (runs idempotently) and run migrations.
echo 'Running Database Migrations'
python3 manage.py migrate_db upgrade
python3 manage.py init_db

# Start the WSGI production server
echo "Starting Application ($ENVIRONMENT)"

if [ "$ENVIRONMENT" = 'development' ]; then
    python3 manage.py runserver
else
    python3 manage.py run_wsgi
fi
