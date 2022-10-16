"""
Users view
"""


from logging import getLogger

from flask import Blueprint, jsonify, request
from flask_expects_json import expects_json
from werkzeug.security import generate_password_hash

from backend import db, user_required
from backend.models.user_models import User
from backend.views.validators import PASSWORD_SCHEMA, USER_UPDATE_SCHEMA

user_blueprint = Blueprint('user', __name__, template_folder='templates')
log = getLogger('mmda-logger')


# READ
@user_blueprint.route('/api/user/<username>/', methods=['GET'])
@user_required
def get_user(username):
    """
    Return details of a user
    """

    # Get User
    user = User.query.filter_by(username=username).first()
    if not user:
        log.debug('No such user %s', username)
        return jsonify({'msg': 'No such user'}), 404

    return jsonify(user.serialize), 200


# PUT
@user_blueprint.route('/api/user/<username>/password/', methods=['PUT'])
@expects_json(PASSWORD_SCHEMA)
@user_required
def put_user_password(username):
    """
    Update a password for a user
    """

    # Check Request
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


# PUT
@user_blueprint.route('/api/user/<username>/', methods=['PUT'])
@expects_json(USER_UPDATE_SCHEMA)
@user_required
def put_user(username):
    """
    Update details of a user
    """

    # Check Request
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')

    # Get User
    user = User.query.filter_by(username=username).first()
    if not user:
        log.debug('No such user %s', username)
        return jsonify({'msg': 'No such user'}), 404

    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    db.session.commit()

    log.debug('Updated details for user %s', user.id)
    return jsonify({'msg': 'Updated'}), 200
