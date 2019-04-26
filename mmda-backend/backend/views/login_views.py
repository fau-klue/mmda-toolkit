"""
Login views
"""


from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_refresh_token_required
from flask_jwt_extended import create_refresh_token, create_access_token
from flask_expects_json import expects_json
from logging import getLogger

from backend.analysis.validators import PASSWORD_SCHEMA
from backend import admin_required, user_required
from backend.models.user_models import User

login_blueprint = Blueprint('login', __name__, template_folder='templates')
log = getLogger('mmda-logger')


@login_blueprint.route('/api/login/', methods=['POST'])
@expects_json(PASSWORD_SCHEMA)
def login():
    """
    Login route to get JWT token to access the API
    """

    # Check Request
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Get User
    user = User.query.filter_by(username=username).first()
    if not user:
        log.debug('No such user %s', username)
        return jsonify({'msg': 'Unauthorized'}), 401

    # Check User
    if not user.is_active:
        log.debug('User %s is deactivated', username)
        return jsonify({'msg': 'Unauthorized'}), 401
    if not current_app.user_manager.verify_password(password, user.password):
        log.debug('Incorrect Password for %s', username)
        return jsonify({'msg': 'Unauthorized'}), 401

    # Create Token
    roles = [role.name for role in user.roles]
    tokens = {
        'current_identity': {'username': username, 'roles': roles},
        'access_token': create_access_token(identity={'username': username, 'roles': roles}),
        'refresh_token': create_refresh_token(identity=username)
    }

    return jsonify(tokens), 200


@login_blueprint.route('/api/refresh/', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """
    Return a new token if the user has a refresh token
    """

    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }

    return jsonify(ret), 200


@login_blueprint.route('/api/test-login/', methods=['GET'])
@jwt_required
def test_login():
    """
    Access the identity of the current user with get_jwt_identity
    """

    ret = {
        'current_identity': get_jwt_identity(),
    }

    return jsonify(ret), 200


@login_blueprint.route('/api/test-login/<username>/', methods=['GET'])
@user_required
def test_user(username):
    """
    Access the username and validate
    """

    ret = {
        'current_identity': get_jwt_identity(),
    }

    return jsonify(ret), 200


@login_blueprint.route('/api/test-admin/', methods=['GET'])
@admin_required
def test_admin():
    """
    Access the roles of the current user with get_jwt_claims
    """

    ret = {
        'current_identity': get_jwt_identity(),
    }

    return jsonify(ret), 200
