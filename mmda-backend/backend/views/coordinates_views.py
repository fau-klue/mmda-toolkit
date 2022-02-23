#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Coordinates view
"""

# requirements
from flask import Blueprint, request, jsonify, current_app
from pandas import DataFrame, notnull
from numpy import nan

# backend
from backend import db
from backend import user_required
from backend.analysis.semspace import generate_semantic_space
from backend.models.user_models import User
from backend.models.analysis_models import Analysis, Coordinates
from backend.models.keyword_models import Keyword

# logging
from logging import getLogger


coordinates_blueprint = Blueprint(
    'coordinates', __name__, template_folder='templates'
)

log = getLogger('mmda-logger')


# READ
@coordinates_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/coordinates/',
    methods=['GET']
)
@user_required
def get_coordinates(username, analysis):
    """ Get coordinates for analysis.

    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('no such analysis %s', analysis)
        return jsonify({'msg': 'no such analysis'}), 404

    # load coordinates
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    df = coordinates.data

    # Workaround: to_dict and jsonify produce invalid JSON with NaN instead of null
    # orient=index means: {"token1":{"user_x":1,"user_y":2,"tsne_x":3,"tsne_y":4}
    df = df.where(notnull(df), None)
    ret = df.to_dict(orient='index')

    return jsonify(ret), 200


# READ
@coordinates_blueprint.route(
    '/api/user/<username>/keyword/<keyword>/coordinates/',
    methods=['GET']
)
@user_required
def get_coordinates_keywords(username, keyword):
    """ Get coordinates for keyword analysis.

    """
    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    keyword = Keyword.query.filter_by(id=keyword, user_id=user.id).first()
    if not keyword:
        log.debug('no such keyword %s', keyword)
        return jsonify({'msg': 'no such keyword'}), 404

    # load coordinates
    coordinates = Coordinates.query.filter_by(keyword_id=keyword.id).first()
    df = coordinates.data

    # Workaround: to_dict and jsonify produce invalid JSON with NaN instead of null
    df = df.where(notnull(df), None)
    # orient=index means: {"token1":{"user_x":1,"user_y":2,"tsne_x":3,"tsne_y":4}
    ret = df.to_dict(orient='index')

    return jsonify(ret), 200


# UPDATE
@coordinates_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/coordinates/reload/',
    methods=['PUT']
)
@user_required
def reload_coordinates(username, analysis):
    """ Re-calculate coordinates for analysis.

    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('no such analysis %s', analysis)
        return jsonify({'msg': 'no such analysis'}), 404

    # get tokens
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    tokens = coordinates.data.index.values

    # generate new coordinates
    log.debug('regenerating semantic space for analysis %s', analysis.id)
    semantic_space = generate_semantic_space(
        tokens,
        current_app.config['CORPORA'][analysis.corpus]['embeddings']
    )

    coordinates.data = semantic_space
    db.session.commit()

    log.debug('updated semantic space for analysis %s', analysis)
    return jsonify({'msg': 'updated'}), 200


@coordinates_blueprint.route(
    '/api/user/<username>/keyword/<keyword>/coordinates/reload/',
    methods=['PUT']
)
@user_required
def reload_coordinates_keywords(username, keyword):
    """ Re-calculate coordinates for keyword analysis.

    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    keyword = Keyword.query.filter_by(id=keyword, user_id=user.id).first()
    if not keyword:
        log.debug('no such keyword analysis %s', keyword)
        return jsonify({'msg': 'no such keyword analysis'}), 404

    # get tokens
    coordinates = Coordinates.query.filter_by(keyword_id=keyword.id).first()
    tokens = coordinates.data.index.values

    # generate new coordinates
    log.debug('regenerating semantic space for analysis %s', keyword.id)
    semantic_space = generate_semantic_space(
        tokens,
        current_app.config['CORPORA'][keyword.corpus]['embeddings']
    )

    coordinates.data = semantic_space
    db.session.commit()

    log.debug('updated semantic space for analysis %s', keyword)
    return jsonify({'msg': 'updated'}), 200


# UPDATE
@coordinates_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/coordinates/',
    methods=['PUT']
)
@user_required
def update_coordinates(username, analysis):
    """ Update coordinates for an analysis.

    Hint: Non numeric values are treated as NaN
    """

    if not request.is_json:
        log.debug('no coordinate data provided')
        return jsonify({'msg': 'no request data provided'}), 400

    # TODO Validate request. Should be:
    # {foo: {user_x: 1, user_y: 2}, bar: {user_x: 1, user_y: 2}}
    items = request.get_json()

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('no such analysis %s', analysis)
        return jsonify({'msg': 'no such analysis'}), 404

    # get coordinates
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    df = coordinates.data

    # update coordinates dataframe, and save
    df.update(DataFrame.from_dict(items, orient='index'))

    # sanity checks, non-numeric get treated as NaN
    df.replace(to_replace=r'[^0-9]+', value=nan, inplace=True, regex=True)

    coordinates.data = df
    db.session.commit()

    log.debug('updated semantic space for analysis %s', analysis)
    return jsonify({'msg': 'updated'}), 200


@coordinates_blueprint.route(
    '/api/user/<username>/keyword/<keyword>/coordinates/',
    methods=['PUT']
)
@user_required
def update_coordinates_keyword(username, keyword):
    """ Update coordinates for an analysis.

    Hint: Non numeric values are treated as NaN
    """

    if not request.is_json:
        log.debug('no coordinate data provided')
        return jsonify({'msg': 'no request data provided'}), 400

    # TODO Validate request. Should be:
    # {foo: {user_x: 1, user_y: 2}, bar: {user_x: 1, user_y: 2}}
    items = request.get_json()

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    keyword = Keyword.query.filter_by(id=keyword, user_id=user.id).first()
    if not keyword:
        log.debug('no such keyword analysis %s', keyword)
        return jsonify({'msg': 'no such keyword analysis'}), 404

    # get coordinates
    coordinates = Coordinates.query.filter_by(keyword_id=keyword.id).first()
    df = coordinates.data

    # update coordinates dataframe, and save
    df.update(DataFrame.from_dict(items, orient='index'))

    # sanity checks, non-numeric get treated as NaN
    df.replace(to_replace=r'[^0-9]+', value=nan, inplace=True, regex=True)

    coordinates.data = df
    db.session.commit()

    log.debug('updated semantic space for keyword analysis %s', keyword)
    return jsonify({'msg': 'updated'}), 200


# DELETE
@coordinates_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/coordinates/',
    methods=['DELETE']
)
@user_required
def delete_coordinates(username, analysis):
    """ Delete coordinates for analysis.

    """

    if not request.is_json:
        log.debug('no coordinate data provided')
        return jsonify({'msg': 'no request data provided'}), 400

    # TODO Validate request. Should be:
    # {foo: {user_x: 1, user_y: 2}, bar: {user_x: 1, user_y: 2}}
    items = request.get_json()

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('no such analysis %s', analysis)
        return jsonify({'msg': 'no such analysis'}), 404

    # get coordinates
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    df = coordinates.data

    for item in items.keys():
        if item in df.index:
            log.debug('removing user coordinates for %s', item)
            df.loc[item]['x_user'] = None
            df.loc[item]['y_user'] = None

    # update coordinates dataframe, and save
    coordinates.data = df
    db.session.commit()

    log.debug('deleted semantic space for analysis %s', analysis)
    return jsonify({'msg': 'deleted'}), 200
