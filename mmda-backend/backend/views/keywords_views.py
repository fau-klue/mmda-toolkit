#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Keywords view
"""

# requirements
from flask import Blueprint, request, jsonify, current_app
# from flask_expects_json import expects_json

# backend
from backend import db
from backend import user_required
# backend.analysis
# from backend.analysis.validators import ANALYSIS_SCHEMA, UPDATE_SCHEMA
from backend.analysis.semspace import generate_semantic_space
from backend.analysis.ccc import ccc_keywords
# backend.models
from backend.models.user_models import User
from backend.models.analysis_models import (
    Keywords, Coordinates
)

# logging
from logging import getLogger


analysis_blueprint = Blueprint(
    'analysis', __name__, template_folder='templates'
)

log = getLogger('mmda-logger')


# CREATE
@analysis_blueprint.route(
    '/api/user/<username>/keywords/',
    methods=['POST']
)
# TODO @expects_json(ANALYSIS_SCHEMA)
@user_required
def create_keywords(username):
    """ Create new analysis for given user.

    parameters:
      - name: username
        type: str

      - name: corpus
        type: str
        description: name of corpus in API
      - name: corpus_reference
        type: str
        description: name of corpus in API

      - name: p
        type: list
        description: p-attributes to query on [lemma]
      - name: p_reference
        type: list
        description: p-attributes to query on [lemma]

      - name: cut_off
        type: int
        description: how many keywords? [None]
        default: 500
      - name: order
        type: str
        description: how to sort them? (column in result table) [log_likelihood]

    responses:
       201:
         description: keywords.id
       400:
         description: "wrong request parameters"
       404:
         description: "empty result"
    """

    user = User.query.filter_by(username=username).first()

    # PARAMETERS #
    # required
    corpus = request.json.get('corpus')
    corpus_reference = request.json.get('corpus_reference')

    # more or less reasonable defaults
    p = request.json.get('p', ['lemma'])
    p_reference = request.json.get('p_reference', ['lemma'])
    flags = request.json.get('flags', '%cd')
    flags_reference = request.json.get('flags_reference', '%cd')

    keyword_analysis_name = request.json.get('name', None)

    # VALIDATION
    for c in [corpus, corpus_reference]:
        if corpus not in current_app.config['CORPORA']:
            msg = 'no corpus "%s"' % c
            log.debug(msg)
            return jsonify({'msg': msg}), 400
    # TODO check p-attributes

    # PROCESS
    log.debug('starting keyword analysis')
    keywords = ccc_keywords(
        corpus_name=corpus,
        corpus_reference=corpus_reference,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        p=p,
        p_reference=p_reference,
        flags=flags,
        flags_reference=flags_reference
    )
    # get tokens for coordinate generation
    log.debug('generating semantic space')
    # TODO: re-implement in backend
    tokens = []
    for df in keywords.values():
        keywords.extend(df.index)
    tokens = list(set(tokens))
    log.debug('extracted %d tokens for analysis semantic space' % len(tokens))

    # error handling: no result?
    if len(tokens) == 0:
        log.debug('no keywords for %s vs. %s' % (corpus, corpus_reference))
        return jsonify({'msg': 'empty result'}), 404

    # generate coordinates
    # dataframe == [token] x y x_user y_user ==
    semantic_space = generate_semantic_space(
        tokens,
        current_app.config['CORPORA'][corpus]['embeddings']
    )

    # SAVE TO DATABASE
    # analysis
    keyword_analysis = Keywords(
        name=keyword_analysis_name,
        corpus=corpus,
        corpus_reference=corpus_reference,
        p=p,
        p_reference=p_reference,
        flags=flags,
        flags_reference=flags_reference,
        user_id=user.id
    )

    db.session.add(keyword_analysis)
    db.session.commit()
    log.debug('added keyword analysis %s to db', keyword_analysis.id)

    # semantic space
    coordinates = Coordinates(
        analysis_id=keyword_analysis.id,
        data=semantic_space
    )
    db.session.add(coordinates)
    db.session.commit()
    log.debug('added coordinates %s to db', coordinates.id)

    return jsonify({'msg': keyword_analysis.id}), 201
