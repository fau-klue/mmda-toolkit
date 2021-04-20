#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Constellation views
"""

# requirements
from flask import Blueprint, request, jsonify, current_app
from flask_expects_json import expects_json
from ccc.utils import cqp_escape

# backend
from backend import db
from backend import user_required
# backend.analysis
from backend.analysis.validators import (
    CONSTELLATION_SCHEMA,
    CONSTELLATION_UPDATE_SCHEMA
)
from backend.analysis.ccc import ccc_concordance
# backend.models
from backend.models.user_models import User
from backend.models.analysis_models import (
    Analysis,
    Discourseme,
    Constellation
)

# logging
from logging import getLogger


constellation_blueprint = Blueprint(
    'constellation', __name__, template_folder='templates'
)

log = getLogger('mmda-logger')


# CREATE
@constellation_blueprint.route(
    '/api/user/<username>/constellation/',
    methods=['POST']
)
@expects_json(CONSTELLATION_SCHEMA)
@user_required
def create_constellation(username):
    """ Create new constellation.

    """

    # Check Request. Discoursemes should be List of IDs
    name = request.json.get('name', None)
    discoursemes = request.json.get('discoursemes', [])

    # Get User
    user = User.query.filter_by(username=username).first()

    # Create Constellation
    constellation = Constellation(name=name, user_id=user.id)
    db.session.add(constellation)
    db.session.commit()
    log.debug('Created Constellation %s', constellation.id)

    for discourseme_id in discoursemes:
        # Check if disourseme exists
        discourseme = Discourseme.query.filter_by(id=discourseme_id, user_id=user.id).first()
        if not discourseme:
            continue

        # Check if exists alread
        constellation_discourseme = discourseme in constellation.discoursemes
        if constellation_discourseme:
            continue

        # Add discourseme link
        constellation.discoursemes.append(discourseme)
        db.session.add(constellation)
        log.debug('Added Discourseme %s to Constellation  %s', discourseme.id, constellation.id)

    db.session.commit()

    return jsonify({'msg': constellation.id}), 201


# READ
@constellation_blueprint.route(
    '/api/user/<username>/constellation/<constellation>/',
    methods=['GET']
)
@user_required
def get_constellation(username, constellation):
    """ Get details for constellation.

    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get from DB
    constellation = Constellation.query.filter_by(id=constellation, user_id=user.id).first()

    if not constellation:
        log.debug('No such Constellation %s', constellation)
        return jsonify({'msg': 'No such constellation'}), 404

    # TODO: Add Discoursemes here as well?
    return jsonify(constellation.serialize), 200


# READ
@constellation_blueprint.route(
    '/api/user/<username>/constellation/',
    methods=['GET']
)
@user_required
def get_constellations(username):
    """ List all constellation for a user.

    """

    # Get User
    user = User.query.filter_by(username=username).first()
    constellations = Constellation.query.filter_by(user_id=user.id).all()
    constellations_list = [constellation.serialize for constellation in constellations]

    return jsonify(constellations_list), 200


# UPDATE
@constellation_blueprint.route(
    '/api/user/<username>/constellation/<constellation>/',
    methods=['PUT']
)
@expects_json(CONSTELLATION_UPDATE_SCHEMA)
@user_required
def update_constellation(username, constellation):
    """ Update constellation details.

    """

    # Check request
    name = request.json.get('name', None)

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Constellation from DB
    constellation = Constellation.query.filter_by(id=constellation, user_id=user.id).first()
    if not constellation:
        log.debug('No such Constellation %s', constellation)
        return jsonify({'msg': 'No such constellation'}), 404

    constellation.name = name
    db.session.commit()
    log.debug('Updated Constellation %s', constellation)

    return jsonify({'msg': constellation.id}), 200


# DELETE
@constellation_blueprint.route('/api/user/<username>/constellation/<constellation>/', methods=['DELETE'])
@user_required
def delete_constellation(username, constellation):
    """
    Delete a constellation.
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Remove Constellation from DB
    constellation = Constellation.query.filter_by(id=constellation, user_id=user.id).first()
    if not constellation:
        log.debug('No such Constellation %s', constellation)
        return jsonify({'msg': 'No such constellation'}), 404

    db.session.delete(constellation)
    db.session.commit()
    log.debug('Deleted Constellation %s', constellation)

    return jsonify({'msg': 'Deleted'}), 200


# READ
@constellation_blueprint.route(
    '/api/user/<username>/constellation/<constellation>/discourseme/',
    methods=['GET']
)
@user_required
def get_discoursemes_for_constellation(username, constellation):
    """ Return list of discoursemes for a constellation constellation.
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Constellation from DB
    constellation = Constellation.query.filter_by(id=constellation, user_id=user.id).first()
    if not constellation:
        log.debug('No such Constellation %s', constellation)
        return jsonify({'msg': 'No such constellation'}), 404

    # Get Discoursemes list from DB
    constellation_discoursemes = [discourseme.serialize for discourseme in constellation.discoursemes]
    if not constellation_discoursemes:
        log.debug('Constellation %s has no Discoursemes associated', constellation.id)
        return jsonify([]), 200

    return jsonify(constellation_discoursemes), 200


# UPDATE
@constellation_blueprint.route(
    '/api/user/<username>/constellation/<constellation>/discourseme/<discourseme>/',
    methods=['PUT']
)
@user_required
def put_discourseme_into_constellation(username, constellation, discourseme):
    """ Put a discourseme into a constellation.

    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Constellation from DB
    constellation = Constellation.query.filter_by(id=constellation, user_id=user.id).first()
    if not constellation:
        log.debug('No such Constellation %s', constellation)
        return jsonify({'msg': 'No such constellation'}), 404

    # Get Discourseme from DB
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        log.debug('No such Discourseme %s', discourseme)
        return jsonify({'msg': 'No such discourseme'}), 404

    # Check if exists
    if discourseme in constellation.discoursemes:
        log.debug('Discourseme %s already linked to Constellation %s', discourseme, constellation)
        return jsonify({'msg': 'Already linked'}), 200

    # Add Link to DB
    constellation.discoursemes.append(discourseme)
    db.session.add(constellation)
    db.session.commit()
    log.debug('Linked Discourseme %s to Constellation %s', discourseme, constellation)

    return jsonify({'msg': 'Updated'}), 200


# DELETE
@constellation_blueprint.route(
    '/api/user/<username>/constellation/<constellation>/discourseme/<discourseme>/',
    methods=['DELETE']
)
@user_required
def delete_discourseme_from_constellation(username, constellation, discourseme):
    """
    Remove a discourseme from a constellation
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Constellation from DB
    constellation = Constellation.query.filter_by(id=constellation, user_id=user.id).first()
    if not constellation:
        log.debug('No such Constellation %s', constellation)
        return jsonify({'msg': 'No such constellation'}), 404

    # Get Discourseme from DB
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        log.debug('No such Discourseme %s', discourseme)
        return jsonify({'msg': 'No such discourseme'}), 404

    if discourseme not in constellation.discoursemes:
        log.debug('Discourseme %s is not linked to Constellation %s', discourseme, constellation)
        return jsonify({'msg': 'Not found'}), 404

    constellation.discoursemes.remove(discourseme)
    db.session.add(constellation)
    db.session.commit()
    log.debug('Unlinked Discourseme %s to Constellation %s', discourseme, constellation)

    return jsonify({'msg': 'Deleted'}), 200


# READ
@constellation_blueprint.route(
    '/api/user/<username>/constellation/<constellation>/concordance/',
    methods=['GET']
)
@user_required
def get_constellation_concordances(username, constellation):
    """ Get concordance lines for a constellation.

    """
    # TODO: rename item ./. items

    # check request
    # ... user
    user = User.query.filter_by(username=username).first()
    # ... analysis
    analysis_id = request.args.get('analysis', None)
    if not analysis_id:
        return jsonify({'msg': 'No analysis provided'}), 400
    analysis = Analysis.query.filter_by(id=analysis_id, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404
    # ... corpora
    corpora = request.args.getlist('corpus', None)
    if not corpora:
        return jsonify({'msg': 'No corpora provided'}), 400
    # get corpus
    corpora_available = current_app.config['CORPORA']
    for corpus in corpora:
        if corpus not in corpora_available.keys():
            return jsonify(
                {'msg': 'No such corpus: {corpus}'.format(corpus=corpus)}
            ), 404
    # ... window size
    window_size = int(request.args.get('window_size', 3))
    # ... optional additional items
    items = [cqp_escape(i) for i in request.args.getlist('item', None)]
    # ... how many?
    cut_off = request.args.get('cut_off', 100)
    # ... how to sort them?
    order = request.args.get('order', 'random')
    # ... where's the meta data?
    s_show = [i for i in request.args.getlist('s_meta', None)]

    # pre-process request
    # ... get associated topic discourseme
    topic_discourseme = Discourseme.query.filter_by(id=analysis.topic_id).first()
    # ... and the whole discourseme constellation
    constellation = Constellation.query.filter_by(
        id=constellation, user_id=user.id
    ).first()
    if not constellation:
        return jsonify({'msg': 'No such Constellation'}), 404
    # ... floating discoursemes
    additional_discoursemes = dict()
    if items:
        # create discourseme for additional items on the fly
        additional_discoursemes['collocate'] = items
    if not constellation.discoursemes:
        log.debug('Constellation %s has no Discoursemes associated', constellation.id)
    else:
        discourseme_ids = [
            d.id for d in constellation.discoursemes if d.id != topic_discourseme.id
        ]
        # get all discoursemes from database and append
        discoursemes = Discourseme.query.filter(
            Discourseme.id.in_(discourseme_ids), Discourseme.user_id == user.id
        ).all()
        for d in discoursemes:
            additional_discoursemes[str(d.id)] = d.items

    # pack p-attributes
    p_show = list(set(['word', analysis.p_query]))

    ret = {}
    for corpus in corpora:

        # use cwb-ccc to extract data
        concordance = ccc_concordance(
            corpus_name=corpus,
            topic_items=topic_discourseme.items,
            topic_name=topic_discourseme.name,
            s_context=analysis.s_break,
            window_size=window_size,
            context=analysis.max_window_size,
            additional_discoursemes=additional_discoursemes,
            p_query=analysis.p_query,
            p_show=p_show,
            s_show=s_show,
            s_query=analysis.s_break,
            order=order,
            cut_off=cut_off
        )

        if concordance is None:
            log.debug('no concordances available for corpus %s', corpus)
            continue

        log.debug(
            'extracted concordances for corpus %s with analysis %s', corpus, analysis
        )

        ret[current_app.config['CORPORA'][corpus]['name']] = concordance

    return jsonify(ret), 200
