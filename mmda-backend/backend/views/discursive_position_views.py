"""
Discursive Position views
"""


from flask import Blueprint, request, jsonify, current_app
from flask_expects_json import expects_json

from backend import db
from backend import user_required
from backend.analysis.validators import DISCURSIVE_POSITION_SCHEMA, UPDATE_SCHEMA
from backend.models.user_models import User
from backend.models.analysis_models import Discourseme, DiscursivePositionDiscoursemes, DiscursivePosition

discursive_blueprint = Blueprint('discursive_position', __name__, template_folder='templates')


# CREATE
@discursive_blueprint.route('/api/user/<username>/discursiveposition/', methods=['POST'])
@expects_json(DISCURSIVE_POSITION_SCHEMA)
@user_required
def create_discursive_position(username):
    """
    Add a new discursive position for a user.
    """

    # Check Request. Discoursemes should be List of IDs
    name = request.json.get('name', None)
    discoursemes = request.json.get('discoursemes', [])

    # Get User
    user = User.query.filter_by(username=username).first()

    # Create Position
    discursive = DiscursivePosition(name=name, user_id=user.id)
    db.session.add(discursive)
    db.session.commit()

    for discourseme_id in discoursemes:
        # Check if disourseme exists
        discourseme = Discourseme.query.filter_by(id=discourseme_id, user_id=user.id).first()
        if not discourseme:
            continue

        # Check if exists alread
        position_discourseme = DiscursivePositionDiscoursemes.query.filter_by(discursive_position_id=discursive.id, discourseme_id=discourseme.id).first()
        if position_discourseme:
            continue

        # Add discourseme link
        position_discourseme = DiscursivePositionDiscoursemes(discursive_position_id=discursive.id, discourseme_id=discourseme.id)
        db.session.add(position_discourseme)

    db.session.commit()

    return jsonify({'msg': discursive.id}), 201


# READ
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/', methods=['GET'])
@user_required
def get_discursive_position(username, discursive_position):
    """
    Get details for a discursive position.
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        return jsonify({'msg': 'No such discursive position'}), 404

    # TODO: Add Discoursemes here as well?
    return jsonify(discursive.serialize), 200


# READ
@discursive_blueprint.route('/api/user/<username>/discursiveposition/', methods=['GET'])
@user_required
def get_discursive_positions(username):
    """
    List all discursive positions for a user.
    """

    # Get User
    user = User.query.filter_by(username=username).first()
    discursives = DiscursivePosition.query.filter_by(user_id=user.id).all()
    discursives_list = [discursive.serialize for discursive in discursives]

    return jsonify(discursives_list), 200


# UPDATE
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/', methods=['PUT'])
@expects_json(UPDATE_SCHEMA)
@user_required
def update_discursive_position(username, discursive_position):
    """
    Update discursive position details
    """

    # Check request
    name = request.json.get('name', None)

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Position from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        return jsonify({'msg': 'No such discursive position'}), 404

    discursive.name = name
    db.session.commit()

    return jsonify({'msg': discursive.id}), 200


# DELETE
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/', methods=['DELETE'])
@user_required
def delete_discursive_position(username, discursive_position):
    """
    Delete a discursive position.
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Remove Position from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        return jsonify({'msg': 'No such discursive position'}), 404

    db.session.delete(discursive)
    db.session.commit()

    return jsonify({'msg': 'Deleted'}), 200


# READ
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/discourseme/', methods=['GET'])
@user_required
def get_discoursemes_for_discursive_position(username, discursive_position):
    """
    Return list of discoursemes for a discursive position
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Position from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        return jsonify({'msg': 'No such discursive position'}), 404

    # Get Discoursemes list from DB
    position_discoursemes = [discourseme.serialize for discourseme in discursive.discourseme]
    if not position_discoursemes:
        return jsonify([]), 200

    return jsonify(position_discoursemes), 200


# UPDATE
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/discourseme/<discourseme>/', methods=['PUT'])
@user_required
def put_discourseme_into_discursive_position(username, discursive_position, discourseme):
    """
    Put a discourseme into a discursive position
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Position from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        return jsonify({'msg': 'No such discursive position'}), 404

    # Get Discourseme from DB
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        return jsonify({'msg': 'No such discourseme'}), 404

    # Check if exists
    position_discourseme = DiscursivePositionDiscoursemes.query.filter_by(discursive_position_id=discursive.id, discourseme_id=discourseme.id).first()

    if position_discourseme:
        return jsonify({'msg': 'Already linked'}), 200

    # Add Link to DB
    position_discourseme = DiscursivePositionDiscoursemes(discursive_position_id=discursive.id, discourseme_id=discourseme.id)
    db.session.add(position_discourseme)
    db.session.commit()

    return jsonify({'msg': 'Updated'}), 200


# DELETE
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/discourseme/<discourseme>/', methods=['DELETE'])
@user_required
def delete_discourseme_from_discursive_position(username, discursive_position, discourseme):
    """
    Remove a discourseme from a discursive position
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Position from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        return jsonify({'msg': 'No such discursive position'}), 404

    # Get Discourseme from DB
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        return jsonify({'msg': 'No such discourseme'}), 404

    position_discourseme = DiscursivePositionDiscoursemes.query.filter_by(discursive_position_id=discursive.id, discourseme_id=discourseme.id).first()

    if not position_discourseme:
        return jsonify({'msg': 'Not found'}), 404

    db.session.delete(position_discourseme)
    db.session.commit()

    return jsonify({'msg': 'Deleted'}), 200


# READ
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/concordances/', methods=['GET'])
@user_required
def get_discursive_position_concordances(username, discursive_position):
    """
    Get concordances for a discursive position.
    """

    # Check Request
    corpora = request.args.getlist('corpus', None)
    items = request.args.getlist('item', None)

    if not items:
        return jsonify({'msg': 'No items provided'}), 400

    if not corpora:
        return jsonify({'msg': 'No corpora provided'}), 400

    # Get Corpus
    corpora_available = current_app.config['CORPORA']
    for corpus in corpora:
        if corpus not in corpora_available.keys():
            return jsonify({'msg': 'No such corpus: {corpus}'.format(corpus=corpus)}), 404

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        return jsonify({'msg': 'No such discursive position'}), 404

    # Get Associated Discoursemes
    discoursemes = [discourseme.serialize for discourseme in discursive.discourseme]
    if not discoursemes:
        return jsonify([]), 200

    discoursemes_items = [discourseme['items'] for discourseme in discoursemes]

    ret = {}
    for corpus in corpora:
        engine = current_app.config['ENGINES'][corpus]
        concordances = engine.extract_discursive_position(items=items, discoursemes=discoursemes_items)
        ret[corpus] = concordances

    return jsonify(ret), 200
