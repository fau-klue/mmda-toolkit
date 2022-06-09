#!/usr/bin/env python3


"""
This file sets up a command line manager.

Use "python manage.py" for a list of available commands.
Use "python manage.py runserver" to start the development web server on localhost:5000.
Use "python manage.py runserver --help" for a list of runserver options.
"""


# from flask_migrate import MigrateCommand
from flask_script import Manager

from backend import create_app
from backend.commands import InitDbCommand, WSGICommand


# Setup Flask-Script with command line commands
manager = Manager(create_app)
# manager.add_command('migrate_db', MigrateCommand)
manager.add_command('init_db', InitDbCommand)
manager.add_command('run_wsgi', WSGICommand)


if __name__ == "__main__":
    manager.run()
