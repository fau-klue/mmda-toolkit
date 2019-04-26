"""
Admin view
"""


import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_expects_json import expects_json
from logging import getLogger

from backend import db
from backend.analysis.validators import PASSWORD_SCHEMA, USER_SCHEMA
from backend.commands.init_db import find_or_create_user
from backend import admin_required
from backend.models.user_models import User, Role
from backend.models.analysis_models import Analysis, Discourseme, DiscursivePosition

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')
log = getLogger('mmda-logger')


# CREATE
@admin_blueprint.route('/api/admin/user/', methods=['POST'])
@expects_json(USER_SCHEMA)
@admin_required
def create_user():
    """
    Admin: Add new user to database
    """

    username = request.json.get('username', None)
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    password = request.json.get('password', None)
    email = request.json.get('email', None)
    email_confirmed_at = request.json.get('email_confirmed_at', datetime.datetime.utcnow())
    role_name = request.json.get('role', None)
    role = None

    if role_name:
        log.debug('Get instance for role %s', role_name)
        role = Role.query.filter(Role.name == role_name).first()
        if not role:
            log.debug('No such role %s', role)
            return jsonify({'msg': 'No such role'}), 404

    log.debug('Create user %s', username)
    user = find_or_create_user(username, first_name, last_name, email, password, role)
    db.session.commit()

    log.debug('User created with ID %s', user.id)
    return jsonify({'msg': user.id}), 201


# READ
@admin_blueprint.route('/api/admin/user/', methods=['GET'])
@admin_required
def get_users():
    """
    Admin: Return a list of all users
    """

    users = User.query.all()
    user_names = [user.username for user in users]

    return jsonify(user_names), 200


# PUT
@admin_blueprint.route('/api/admin/user/<username>/password/', methods=['PUT'])
@expects_json(PASSWORD_SCHEMA)
@admin_required
def put_user_password(username):
    """
    Admin: Update a password for a user
    """

    new_password = request.json.get('password')

    # Get User
    user = User.query.filter_by(username=username).first()
    if not user:
        log.debug('No such user %s', username)
        return jsonify({'msg': 'No such user'}), 404

    # Generate salted password hash
    hashed_password = current_app.user_manager.password_manager.hash_password(new_password)

    if not hashed_password:
        log.debug('Password could not be changed. No hash generated')
        return jsonify({'msg': 'Password could not be changed'}), 500

    # Only set if we got a valid hash
    user.password = hashed_password
    db.session.commit()

    log.debug('Password updated for user %s', user.id)
    return jsonify({'msg': 'Updated'}), 200


# DELETE
@admin_blueprint.route('/api/admin/user/<username>/', methods=['DELETE'])
@admin_required
def delete_user(username):
    """
    Admin: Delete a user
    """

    # Get User
    user = User.query.filter_by(username=username).first()
    if not user:
        log.debug('No such user %s', username)
        return jsonify({'msg': 'No such user'}), 404

    # Cannot delete admin
    if user.username == 'admin':
        return jsonify({'msg': 'Cannot delete'}), 409

    db.session.delete(user)
    db.session.commit()

    log.debug('Deleted user %s', username)
    return jsonify({'msg': 'Deleted'}), 200


# READ
@admin_blueprint.route('/api/admin/analysis/', methods=['GET'])
@admin_required
def get_analysis():
    """
    Admin: List all analysis
    """

    items = Analysis.query.all()
    items_serial = [item.serialize for item in items]

    return jsonify(items_serial), 200


# READ
@admin_blueprint.route('/api/admin/discourseme/', methods=['GET'])
@admin_required
def get_discourseme():
    """
    Admin: List all discoursme
    """

    items = Discourseme.query.all()
    items_serial = [item.serialize for item in items]

    return jsonify(items_serial), 200



# READ
@admin_blueprint.route('/api/admin/discursiveposition/', methods=['GET'])
@admin_required
def get_discursive_position():
    """
    Admin: List all discursive position
    """

    items = DiscursivePosition.query.all()
    items_serial = [item.serialize for item in items]

    return jsonify(items_serial), 200


# DELETE
@admin_blueprint.route('/api/admin/analysis/<analysis>/', methods=['DELETE'])
@admin_required
def delete_analysis(analysis):
    """
    Admin: Remove an Analysis
    """

    item = Analysis.query.filter_by(id=analysis).first()
    if not item:
        log.debug('No such item %s', analysis)
        return jsonify({'msg': 'No such item'}), 404

    db.session.delete(item)
    db.session.commit()

    log.debug('Deleted analysis %s', analysis)
    return jsonify({'msg': 'Deleted'}), 200


# DELETE
@admin_blueprint.route('/api/admin/discourseme/<discourseme>/', methods=['DELETE'])
@admin_required
def delete_discourseme(discourseme):
    """
    Admin: Remove a Discourseme
    """

    item = Discourseme.query.filter_by(id=discourseme).first()
    if not item:
        log.debug('No such item %s', discourseme)
        return jsonify({'msg': 'No such item'}), 404

    db.session.delete(item)
    db.session.commit()

    log.debug('Deleted discourseme %s', discourseme)
    return jsonify({'msg': 'Deleted'}), 200



# DELETE
@admin_blueprint.route('/api/admin/discursiveposition/<discursive_position>/', methods=['DELETE'])
@admin_required
def delete_discursive_position(discursive_position):
    """
    Admin: Remove a discursive position
    """

    item = DiscursivePosition.query.filter_by(id=discursive_position).first()
    if not item:
        log.debug('No such item %s', discursive_position)
        return jsonify({'msg': 'No such item'}), 404

    db.session.delete(item)
    db.session.commit()

    log.debug('Deleted position %s', discursive_position)
    return jsonify({'msg': 'Deleted'}), 200
