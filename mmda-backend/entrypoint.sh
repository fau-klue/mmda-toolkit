#!/usr/bin/env sh
# Entrypoint for Docker

# Initialize database (runs idempotently) and run migrations.
echo 'Running Database Migrations'
python3 manage.py db upgrade
python3 manage.py init_db

# Start the WSGI production server
echo 'Staring Application'
python3 manage.py run_wsgi
