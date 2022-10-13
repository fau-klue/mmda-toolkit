#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from flask import Blueprint, current_app
from werkzeug.security import generate_password_hash

from backend import db
from backend.models.user_models import Role, User

bp = Blueprint('database', __name__, url_prefix='/database')


def db_exists():
    """
    Check if database is already initialised.
    """

    tables = db.inspect(db.get_engine()).get_table_names()
    return True if 'users' in tables else False


def init_db():
    """
    Initialise the database.
    """

    if not db_exists():
        db.drop_all()
        db.create_all()

    create_users()


def create_users():
    """
    Create users
    """

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')

    # Add users
    find_or_create_user(u'admin', u'Admin', u'MMDA', u'admin@fau.de', 'CCL-Erlangen$2022', admin_role)
    find_or_create_user(u'student1', u'Student', u'Example', u'student@fau.de', 'Erlangen1')

    # Save to DB
    db.session.commit()


def find_or_create_role(name, description):
    """
    Find existing role or create new role

    :param str name: Name of the role
    :param str description: Description of the role
    :return: Role Object for this role
    :rtype: Role
    """

    role = Role.query.filter(Role.name == name).first()

    if not role:
        role = Role(name=name, description=description)
        db.session.add(role)

    return role


def find_or_create_user(username, first_name, last_name, email, password, role=None):
    """
    Find existing user or create new user
    role must be of type Role.

    :param str username: Username of the user
    :param str first_name: First Name of the user
    :param str last_name: Last Name of the user
    :param str email: Email of the user
    :param str password: Password in clear (will get encrypted/salted)
    :param Role role: Role for this user
    :return: User Object
    :rtype: User
    """

    user = User.query.filter(User.email == email).first()

    if not user:
        user = User(username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=generate_password_hash(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)

    return user


@bp.cli.command('init')
def init_db_command():
    """Clear the existing data and create new tables."""

    current_app.logger.info(f"Database path: {current_app.config['SQLALCHEMY_DATABASE_URI']}")
    init_db()
    current_app.logger.info("Database has been initialised.")
