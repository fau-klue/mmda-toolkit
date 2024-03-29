"""
Admin view
"""


from logging import getLogger

from flask import Blueprint, jsonify, request
from flask_expects_json import expects_json
from werkzeug.security import generate_password_hash

from backend import admin_required, db
from backend.database import find_or_create_user
from backend.models.collocation_models import Collocation
from backend.models.discourseme_models import Constellation, Discourseme
from backend.models.keyword_models import Keyword
from backend.models.user_models import Role, User
from backend.views.validators import PASSWORD_SCHEMA, USER_SCHEMA

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
    # email_confirmed_at = request.json.get('email_confirmed_at', datetime.datetime.utcnow())
    role_name = request.json.get('role', None)
    role = None

    if role_name:
        log.debug('Get instance for role %s', role_name)
        role = Role.query.filter(Role.name == role_name).first()
        if not role:
            log.debug('No such role %s', role)
            return jsonify({'msg': 'No such role'}), 404

    # Check if username exists
    if User.query.filter_by(username=username).first():
        log.debug('User %s already exists', username)
        return jsonify({'msg': 'User already exists'}), 409

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
    hashed_password = generate_password_hash(new_password)

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
@admin_blueprint.route('/api/admin/collocation/', methods=['GET'])
@admin_required
def get_collocation():
    """
    Admin: List all collocation analyses
    """

    items = Collocation.query.all()
    items_serial = [item.serialize for item in items]

    return jsonify(items_serial), 200


# READ
@admin_blueprint.route('/api/admin/keyword/', methods=['GET'])
@admin_required
def get_keyword():
    """
    Admin: List all keyword analyses
    """

    items = Keyword.query.all()
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
@admin_blueprint.route('/api/admin/constellation/', methods=['GET'])
@admin_required
def get_constellation():
    """
    Admin: List all constellation
    """

    items = Constellation.query.all()
    items_serial = [item.serialize for item in items]

    return jsonify(items_serial), 200


# DELETE
@admin_blueprint.route('/api/admin/collocation/<collocation>/', methods=['DELETE'])
@admin_required
def delete_collocation(collocation):
    """
    Admin: Remove a Collocation Analysis
    """

    item = Collocation.query.filter_by(id=collocation).first()
    if not item:
        log.debug('No such item %s', collocation)
        return jsonify({'msg': 'No such item'}), 404

    db.session.delete(item)
    db.session.commit()

    log.debug('Deleted collocation analysis %s', collocation)
    return jsonify({'msg': 'Deleted'}), 200


# DELETE
@admin_blueprint.route('/api/admin/keyword/<keyword>/', methods=['DELETE'])
@admin_required
def delete_keyword(keyword):
    """
    Admin: Remove a Keyword Analysis
    """

    item = Keyword.query.filter_by(id=keyword).first()
    if not item:
        log.debug('No such item %s', keyword)
        return jsonify({'msg': 'No such item'}), 404

    db.session.delete(item)
    db.session.commit()

    log.debug('Deleted keyword analysis %s', keyword)
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
@admin_blueprint.route('/api/admin/constellation/<constellation>/', methods=['DELETE'])
@admin_required
def delete_constellation(constellation):
    """
    Admin: Remove a constellation
    """

    item = Constellation.query.filter_by(id=constellation).first()
    if not item:
        log.debug('No such item %s', constellation)
        return jsonify({'msg': 'No such item'}), 404

    db.session.delete(item)
    db.session.commit()

    log.debug('Deleted constellation %s', constellation)
    return jsonify({'msg': 'Deleted'}), 200
