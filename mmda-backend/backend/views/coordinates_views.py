# Coordinates view

from pandas import notnull, DataFrame
from flask import Blueprint, redirect, render_template
from flask import request, url_for, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend import db, cache
from backend import admin_required, user_required
from backend.analysis.coordinates.tsne import generate_semantic_space
from backend.models.user_models import User
from backend.models.analysis_models import Analysis, AnalysisDiscoursemes, Discourseme, Coordinates

coordinates_blueprint = Blueprint('coordinates', __name__, template_folder='templates')


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
        return jsonify({'msg': 'No such analysis'}), 404

    # Get the current coordinates and tokens
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    df = coordinates.data
    tokens = df.index.values

    # Generate new coordinates
    wectors_path = current_app.config['CORPORA'][analysis.corpus]['wectors']
    semantic_space = generate_semantic_space(tokens, wectors_path)

    coordinates.data = semantic_space
    db.session.commit()

    return jsonify({'msg': 'Updated'}), 200


# UPDATE
@coordinates_blueprint.route('/api/user/<username>/analysis/<analysis>/coordinates/', methods=['PUT'])
@user_required
def update_coordinates(username, analysis):
    """
    Update the coordinates for an analysis.
    To Change user_x and user_y.
    """

    if not request.is_json:
        return jsonify({'msg': 'No request data provided'}), 400

    # TODO Validate request. Should be:
    # {foo: {user_x: 1, user_y: 2}, bar: {user_x: 1, user_y: 2}}
    items = request.get_json()

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Analysis from DB
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        return jsonify({'msg': 'No such analysis'}), 404

    # Load Coordinates from DB
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    df = coordinates.data

    # Update coordinates dataframe, and save
    df.update(DataFrame.from_dict(items, orient='index'))
    coordinates.data = df

    db.session.commit()

    return jsonify({'msg': 'Updated'}), 200
