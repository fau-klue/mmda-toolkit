"""
Admin view
"""


import datetime
from flask import Blueprint, request, jsonify, current_app

from backend import db
from backend.commands.init_db import find_or_create_user
from backend import admin_required
from backend.models.user_models import User
from backend.models.analysis_models import Analysis, Discourseme, DiscursivePosition

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


def valid(username, first_name, last_name, email, password):
    """
    Check if data is provided and is correct.
    """

    if len(password) < current_app.config['USER_MIN_PASSWORD_LENGTH']:
        return False

    return bool(username and first_name and last_name and email and password)


# CREATE
@admin_blueprint.route('/api/admin/user/', methods=['POST'])
@admin_required
def create_user():
    """
    Admin: Add new user to database
    """

    if not request.is_json:
        return jsonify({'msg': 'No request data provided'}), 400

    # TODO: Validate JSON (alphanum, email Regex)
    username = request.json.get('username', None)
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    password = request.json.get('password', None)
    email = request.json.get('email', None)
    email_confirmed_at = request.json.get('email_confirmed_at', datetime.datetime.utcnow())
    role = request.json.get('role', None)

    if not valid(username, first_name, last_name, email, password):
        return jsonify({'msg': 'Incorrect request data provided'}), 400

    # Create user
    user = find_or_create_user(username, first_name, last_name, email, password, role)

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
@admin_required
def put_user_password(username):
    """
    Admin: Update a password for a user
    """

    if not request.is_json:
        return jsonify({'msg': 'No request data provided'}), 400

    # Check Request
    new_password = request.json.get('password')
    if not new_password or len(new_password) < current_app.config['USER_MIN_PASSWORD_LENGTH']:
        return jsonify({'msg': 'Incorrect request data provided'}), 400

    # Get User
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'msg': 'No such user'}), 404

    # Generate salted password hash
    hashed_password = current_app.user_manager.password_manager.hash_password(new_password)

    if not hashed_password:
        return jsonify({'msg': 'Password could not be changed'}), 500

    # Only set if we got a valid hash
    user.password = hashed_password
    db.session.commit()

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
        return jsonify({'msg': 'No such user'}), 404

    # Cannot delete admin
    if user.username == 'admin':
        return jsonify({'msg': 'Cannot delete'}), 409

    db.session.delete(user)
    db.session.commit()

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
        return jsonify({'msg': 'No such item'}), 404

    db.session.delete(item)
    db.session.commit()

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
        return jsonify({'msg': 'No such item'}), 404

    db.session.delete(item)
    db.session.commit()

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
        return jsonify({'msg': 'No such item'}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({'msg': 'Deleted'}), 200
