"""
Coordinates view
"""


from pandas import notnull, DataFrame
from numpy import nan

from flask import Blueprint, request, jsonify, current_app
from logging import getLogger

from backend import db
from backend import user_required
from backend.analysis.semspace import generate_semantic_space
from backend.models.user_models import User
from backend.models.analysis_models import Analysis, Coordinates

coordinates_blueprint = Blueprint('coordinates', __name__, template_folder='templates')
log = getLogger('mmda-logger')


# READ
@coordinates_blueprint.route('/api/user/<username>/analysis/<analysis>/coordinates/', methods=['GET'])
@user_required
def get_coordinates(username, analysis):
    """
    Get the coordinates for an analysis
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Analysis from DB
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Load Coordinates from DB
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    df = coordinates.data

    # Workaround: to_dict and jsonify produce invalid JSON with NaN instead of null
    # orient=index means: {"token1":{"user_x":1,"user_y":2,"tsne_x":3,"tsne_y":4}
    df = df.where(notnull(df), None)
    ret = df.to_dict(orient='index')

    return jsonify(ret), 200


# UPDATE
@coordinates_blueprint.route('/api/user/<username>/analysis/<analysis>/coordinates/reload/', methods=['PUT'])
@user_required
def reload_coordinates(username, analysis):
    """
    Reloads the coodinates for an analysis
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Analysis from DB
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Get the current coordinates and tokens
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    df = coordinates.data
    tokens = df.index.values

    # Generate new coordinates
    log.debug('Regenerating semantic space for analysis %s', analysis.id)
    wectors_path = current_app.config['CORPORA'][analysis.corpus]['wectors']
    semantic_space = generate_semantic_space(tokens, wectors_path)

    coordinates.data = semantic_space
    db.session.commit()

    log.debug('Updated semantic space for analysis %s', analysis)
    return jsonify({'msg': 'Updated'}), 200


# UPDATE
@coordinates_blueprint.route('/api/user/<username>/analysis/<analysis>/coordinates/', methods=['PUT'])
@user_required
def update_coordinates(username, analysis):
    """
    Update the coordinates for an analysis.
    To change user_x and user_y.
    Hint: Non numeric values are treated as NaN
    """

    if not request.is_json:
        log.debug('No coordinate data provided')
        return jsonify({'msg': 'No request data provided'}), 400

    # TODO Validate request. Should be:
    # {foo: {user_x: 1, user_y: 2}, bar: {user_x: 1, user_y: 2}}
    items = request.get_json()

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Analysis from DB
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Load Coordinates from DB
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    df = coordinates.data

    # Update coordinates dataframe, and save
    df.update(DataFrame.from_dict(items, orient='index'))

    # Sanity checks, non-numeric get treated as NaN
    df.replace(to_replace=r'[^0-9]+', value=nan, inplace=True, regex=True)

    coordinates.data = df
    db.session.commit()

    log.debug('Updated semantic space for analysis %s', analysis)
    return jsonify({'msg': 'Updated'}), 200


# DELETE
@coordinates_blueprint.route('/api/user/<username>/analysis/<analysis>/coordinates/', methods=['DELETE'])
@user_required
def delete_coordinates(username, analysis):
    """
    delete the coordinates for an analysis.
    To change user_x and user_y.
    """

    if not request.is_json:
        log.debug('No coordinate data provided')
        return jsonify({'msg': 'No request data provided'}), 400

    # TODO Validate request. Should be:
    # {foo: {user_x: 1, user_y: 2}, bar: {user_x: 1, user_y: 2}}
    items = request.get_json()

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Analysis from DB
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Load Coordinates from DB
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    df = coordinates.data

    for item in items.keys():
        if item in df.index:
            log.debug('Removing user coordinates for %s', item)
            df.loc[item]['user_x'] = None
            df.loc[item]['user_y'] = None

    # Update coordinates dataframe, and save
    coordinates.data = df
    db.session.commit()

    log.debug('Updated semantic space for analysis %s', analysis)
    return jsonify({'msg': 'Deleted'}), 200
