"""
Users view
"""


from flask import Blueprint, request, jsonify, current_app

from backend import db
from backend import user_required
from backend.models.user_models import User

user_blueprint = Blueprint('user', __name__, template_folder='templates')


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
        return jsonify({'msg': 'No such user'}), 404

    return jsonify(user.serialize), 200


# PUT
@user_blueprint.route('/api/user/<username>/password/', methods=['PUT'])
@user_required
def put_user_password(username):
    """
    Update a password for a user
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
