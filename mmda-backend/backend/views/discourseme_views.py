"""
Discourseme view
"""


from flask import Blueprint, request, jsonify
from flask_expects_json import expects_json

from backend import db
from backend import user_required
from backend.analysis.validators import DISCOURSEME_SCHEMA
from backend.models.user_models import User
from backend.models.analysis_models import Discourseme

discourseme_blueprint = Blueprint('discourseme', __name__, template_folder='templates')


# CREATE
@discourseme_blueprint.route('/api/user/<username>/discourseme/', methods=['POST'])
@expects_json(DISCOURSEME_SCHEMA)
@user_required
def create_discourseme(username):
    """
    Create a new discourseme
    """

    # Check request
    name = request.json.get('name', None)
    items = request.json.get('items', [])

    # Get User
    user = User.query.filter_by(username=username).first()

    # Add Discourseme to DB
    discourseme = Discourseme(name=name, items=items, user_id=user.id)
    db.session.add(discourseme)
    db.session.commit()

    return jsonify({'msg': discourseme.id}), 201


# READ
@discourseme_blueprint.route('/api/user/<username>/discourseme/', methods=['GET'])
@user_required
def get_discoursemes(username):
    """
    List associated discoursemes for an user
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    discoursemes = Discourseme.query.filter_by(user_id=user.id).all()
    discoursemes_list = [discourseme.serialize for discourseme in discoursemes]

    return jsonify(discoursemes_list), 200


# READ
@discourseme_blueprint.route('/api/user/<username>/discourseme/<discourseme>/', methods=['GET'])
@user_required
def get_discourseme(username, discourseme):
    """
    Get the details for a discourseme
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Discourseme from DB
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        return jsonify({'msg': 'No such discourseme'}), 404

    return jsonify(discourseme.serialize), 200


# UPDATE
@discourseme_blueprint.route('/api/user/<username>/discourseme/<discourseme>/', methods=['PUT'])
@expects_json(DISCOURSEME_SCHEMA)
@user_required
def update_discourseme(username, discourseme):
    """
    Update the details of a discourseme
    """

    # Check Request
    name = request.json.get('name', None)
    items = request.json.get('items', [])

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Discourseme from DB
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()

    if discourseme.topic:
        return jsonify({'msg': 'Cannot edit topic discourseme'}), 409

    discourseme.name = name
    discourseme.items = items
    db.session.commit()

    return jsonify({'msg': discourseme.id}), 200


# DELETE
@discourseme_blueprint.route('/api/user/<username>/discourseme/<discourseme>/', methods=['DELETE'])
@user_required
def delete_discourseme(username, discourseme):
    """
    Delete a discourseme
    """

   # Get User
    user = User.query.filter_by(username=username).first()

    # Get Discourseme from DB
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        return jsonify({'msg': 'No such discourseme'}), 404

    # Check if topic, cause you cant delete these without deleting the analysis
    if discourseme.topic:
        return jsonify({'msg': 'Cannot delete topic discourseme'}), 409

    db.session.delete(discourseme)
    db.session.commit()

    return jsonify({'msg': 'Deleted'}), 200
