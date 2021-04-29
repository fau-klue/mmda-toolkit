#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Analysis view
"""

# requirements
from flask import Blueprint, request, jsonify, current_app
from flask_expects_json import expects_json
from ccc.utils import cqp_escape

# backend
from backend import db
from backend import user_required
# backend.analysis
from backend.analysis.validators import ANALYSIS_SCHEMA, UPDATE_SCHEMA
from backend.analysis.semspace import generate_semantic_space
from backend.analysis.ccc import ccc_concordance, ccc_collocates, ccc_breakdown
# backend.models
from backend.models.user_models import User
from backend.models.analysis_models import (
    Analysis, Discourseme, Coordinates
)

# logging
from logging import getLogger


analysis_blueprint = Blueprint(
    'analysis', __name__, template_folder='templates'
)

log = getLogger('mmda-logger')


############
# ANALYSIS #
############

# CREATE
@analysis_blueprint.route(
    '/api/user/<username>/analysis/',
    methods=['POST']
)
@expects_json(ANALYSIS_SCHEMA)
@user_required
def create_analysis(username):
    """ Create new analysis for given user.

    parameters:
      - username: username
        type: str
        description: username, links to user
      - name: name
        type: str
        description: analysis name
      - corpus_name: corpus_name
        type: str
        description: name of corpus
      - name: context
        type: int
        description: context size in tokens [10]
      - name: p_query
        type: str
        description: p-attribute to query on [lemma]
      - name: s_break
        type: str
        description: s-attribute to break context at
      - name: items
        type: list
        description: topic items
      - name: cut_off
        type: int
        description: how many collocates? [200]
      - name: order
        type: str
        description: how to sort them? (column in result table) [log_likelihood]
    responses:
       201:
         description: analysis.id
       400:
         description: "wrong request parameters"
       404:
         description: "empty result"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # check this
    discourseme = request.json.get('discourseme', None)
    analysis_name = request.json.get('name', None)
    print(discourseme)

    # check request
    corpus_name = request.json.get('corpus', None)
    context = request.json.get('context', 10)
    p_query = request.json.get('p_query', 'lemma')
    p_analysis = request.json.get('p_analysis', 'lemma')
    s_break = request.json.get('s_break', 'text')
    items = request.json.get('items', [])

    # not set yet
    cut_off = request.json.get('cut_off', 200)
    order = request.json.get('order', 'log_likelihood')
    flags_query = "%cd"
    escape = False
    flags_show = ""
    p_show = [p_analysis]
    min_freq = 2
    ams = request.json.get('ams', None)

    # check corpus
    if corpus_name not in current_app.config['CORPORA']:
        log.debug('no such corpus "%s"', corpus_name)
        return jsonify({'msg': 'no such corpus'}), 400

    # create new discourseme if necessary
    if isinstance(discourseme, str):
        topic_discourseme = Discourseme(
            name=discourseme,
            items=items,
            user_id=user.id
        )
        db.session.add(topic_discourseme)
        db.session.commit()
        log.debug('created discourseme %s', topic_discourseme.id)
    elif isinstance(discourseme, dict):
        topic_discourseme = Discourseme.query.filter_by(
            id=discourseme['id']
        ).first()
    else:
        return jsonify({
            'msg': "discourseme of type %s" % str(type(discourseme))
        }), 400

    # collocates: dict of dataframes with key == window_size
    log.debug('starting collocation analysis')
    collocates = ccc_collocates(
        corpus_name=corpus_name,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        topic_items=items,
        s_context=s_break,
        windows=range(1, context),
        context=context,
        p_query=p_query,
        flags_query=flags_query,
        s_query=s_break,
        p_show=p_show,
        flags_show=flags_show,
        ams=ams,
        cut_off=cut_off,
        min_freq=min_freq,
        order=order,
        escape=escape
    )

    # get tokens for coordinate generation
    # TODO: re-implement in backend
    tokens = []
    for df in collocates.values():
        tokens.extend(df.index)
    tokens = list(set(tokens))
    log.debug('extracted %d tokens for analysis semantic space' % len(tokens))

    # error handling: no result?
    if len(tokens) == 0:
        log.debug('no collocates for query found for %s', items)
        return jsonify({'msg': 'empty result'}), 404

    # generate coordinates
    log.debug('generating semantic space')
    semantic_space = generate_semantic_space(
        tokens,
        current_app.config['CORPORA'][corpus_name]['embeddings']
    )

    # add analysis to db
    analysis = Analysis(
        name=analysis_name,
        corpus=corpus_name,
        p_query=p_query,
        p_analysis=p_analysis,
        s_break=s_break,
        context=context,
        items=items,
        topic_id=topic_discourseme.id,
        user_id=user.id,
    )
    db.session.add(analysis)
    db.session.commit()
    log.debug('added analysis %s to db', analysis.id)

    coordinates = Coordinates(analysis_id=analysis.id)
    coordinates.data = semantic_space
    db.session.add(coordinates)
    db.session.commit()
    log.debug('added coordinates %s to db', coordinates.id)

    return jsonify({'msg': analysis.id}), 201


# READ ALL
@analysis_blueprint.route(
    '/api/user/<username>/analysis/',
    methods=['GET']
)
@user_required
def get_all_analysis(username):
    """ List all analyses for given user.

    parameters:
      - username: username
        type: str
        description: username, links to user
    responses:
      200:
         description: list of serialized analyses
    """

    # get user
    user = User.query.filter_by(username=username).first()

    analyses = Analysis.query.filter_by(user_id=user.id).all()
    analyses_list = [analysis.serialize for analysis in analyses]

    return jsonify(analyses_list), 200


# READ
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/',
    methods=['GET']
)
@user_required
def get_analysis(username, analysis):
    """ Get details of analysis.

    parameters:
      - username: username
        type: str
        description: username, links to user
      - name: analysis
        type: str
        description: analysis id
    responses:
       200:
         description: dict of analysis details
       404:
         description: "no such analysis"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('no such analysis %s', analysis)
        return jsonify({'msg': 'no such analysis'}), 404

    return jsonify(analysis.serialize), 200


# UPDATE
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/',
    methods=['PUT']
)
@expects_json(UPDATE_SCHEMA)
@user_required
def update_analysis(username, analysis):
    """ Edit analysis.

    parameters:
      - username: username
        type: str
        description: username, links to user
      - name: analysis
        type: str
        description: analysis id
      - name: name
        type: str
        description: new analysis name
    responses:
       200:
         description: analysis.id
       400:
         description: "wrong request parameters"
    """
    # get user
    user = User.query.filter_by(username=username).first()
    # check request
    name = request.json.get('name', None)
    if not name:
        log.debug('no name provided for analysis %s', analysis)
        return jsonify({'msg': 'wrong request parameters'}), 400

    # update analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    analysis.name = name
    db.session.commit()

    log.debug('updated analysis with ID %s', analysis)
    return jsonify({'msg': analysis.id}), 200


# DELETE
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/',
    methods=['DELETE']
)
@user_required
def delete_analysis(username, analysis):
    """ Delete analysis.

    parameters:
      - username: username
        type: str
        description: username, links to user
      - name: analysis
        type: str
        description: analysis id
    responses:
       200:
         description: "deleted"
       404:
         description: "no such analysis"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # delete analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('no such analysis %s', analysis)
        return jsonify({'msg': 'no such analysis'}), 404

    db.session.delete(analysis)
    db.session.commit()

    log.debug('deleted analysis with ID %s', analysis)
    return jsonify({'msg': 'deleted'}), 200


###########################
# ASSOCIATED DISCOURSEMES #
###########################

# READ
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/discourseme/',
    methods=['GET']
)
@user_required
def get_discoursemes_for_analysis(username, analysis):
    """ Return list of discoursemes for analysis.

    parameters:
      - username: username
        type: str
        description: username, links to user
      - name: analysis
        type: str
        description: analysis id
    responses:
       200:
         description: list of associated discoursemes
       404:
         description: "no such analysis"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('no such analysis %s', analysis)
        return jsonify({'msg': 'no such analysis'}), 404

    # get discoursemes as list
    analysis_discoursemes = [
        discourseme.serialize for discourseme in analysis.discoursemes
    ]
    if not analysis_discoursemes:
        log.debug('no disoursemes associated')
        return jsonify([]), 200

    return jsonify(analysis_discoursemes), 200


# UPDATE
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/discourseme/<discourseme>/',
    methods=['PUT']
)
@user_required
def put_discourseme_into_analysis(username, analysis, discourseme):
    """ Associate a discourseme with an analysis.

    parameters:
      - name: username
        type: str
        description: username, links to user
      - name: analysis
        type: int
        description: analysis id
      - name: discourseme
        type: int
        description: discourseme id to associate
    responses:
      200:
         description: "already linked"
         description: "updated"
      404:
         description: "no such analysis"
         description: "no such discourseme"
      409:
         description: "discourseme is already topic of analysis"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        msg = 'no such analysis %s' % analysis
        log.debug(msg)
        return jsonify({'msg': msg}), 404

    # get discourseme
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        msg = 'no such discourseme %s' % discourseme
        log.debug(msg)
        return jsonify({'msg': msg}), 404

    # check if already linked or discourseme is topic discourseme of analysis
    analysis_discourseme = discourseme in analysis.discoursemes
    is_own_topic_discourseme = discourseme.id == analysis.topic_id
    if is_own_topic_discourseme:
        msg = 'discourseme %s is already topic of the analysis', discourseme
        log.debug(msg)
        return jsonify({'msg': msg}), 409
    if analysis_discourseme:
        msg = 'discourseme %s is already associated', discourseme
        log.debug(msg)
        return jsonify({'msg': msg}), 200

    # # collocates: dict of dataframes with key == window_size
    # log.debug('starting collocation analysis')
    # collocates = ccc_collocates(
    #     corpus_name=corpus_name,
    #     cqp_bin=current_app.config['CCC_CQP_BIN'],
    #     registry_path=current_app.config['CCC_REGISTRY_PATH'],
    #     data_path=current_app.config['CCC_DATA_PATH'],
    #     lib_path=current_app.config['CCC_LIB_PATH'],
    #     topic_items=items,
    #     s_context=s_break,
    #     windows=range(1, context),
    #     context=context,
    #     p_query=p_query,
    #     flags_query=flags_query,
    #     s_query=s_break,
    #     p_show=p_show,
    #     flags_show=flags_show,
    #     ams=ams,
    #     cut_off=cut_off,
    #     min_freq=min_freq,
    #     order=order,
    #     escape=escape
    # )

    # # new coordinates
    # log.debug('generating coordinates for missing items')
    # coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    # semantic_space = coordinates.data
    # new_coordinates = generate_discourseme_coordinates(
    #     discourseme.items,
    #     semantic_space,
    #     current_app.config['CORPORA'][analysis.corpus]['embeddings']
    # )
    # if not new_coordinates.empty:
    #     log.debug('appending new coordinates to semantic space')
    #     semantic_space.append(new_coordinates, sort=True)
    #     coordinates.data = semantic_space
    # db.session.commit()
    # collocates: dict of dataframes with key == window_size
    # collocates = ccc_collocates(
    #     corpus_name=analysis.corpus,
    #     cqp_bin=current_app.config['CCC_CQP_BIN'],
    #     registry_path=current_app.config['CCC_REGISTRY_PATH'],
    #     data_path=current_app.config['CCC_DATA_PATH'],
    #     lib_path=current_app.config['CCC_LIB_PATH'],
    #     topic_items=analysis.items,
    #     s_context=analysis.s_break,
    #     window_sizes=range(1, analysis.context),
    #     context=analysis.context,
    #     p_query=analysis.p_query,
    #     additional_discoursemes={str(discourseme.id): discourseme.items},
    #     s_query=None,
    #     ams=None,
    #     cut_off=200,
    #     order='log_likelihood'
    # )

    # # get tokens for coordinate generation
    # # TODO: reimplement in backend
    # tokens = []
    # for df in collocates.values():
    #     tokens.extend(df.index)
    # tokens = list(set(tokens))
    # log.debug('extracted %d tokens for analysis %s' % (len(tokens), analysis.id))

    # log.debug('generating coordinates for missing collocates')
    # coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    # semantic_space = coordinates.data
    # new_coordinates = generate_discourseme_coordinates(
    #     discourseme.items,
    #     semantic_space,
    #     current_app.config['CORPORA'][analysis.corpus]['embeddings']
    # )
    # if not new_coordinates.empty:
    #     log.debug('appending new coordinates to semantic space')
    #     semantic_space.append(new_coordinates, sort=True)
    #     coordinates.data = semantic_space
    # db.session.commit()

    # log.debug('added discourseme %s to analysis %s', discourseme, analysis)
    # return jsonify({'msg': 'updated'}), 200

    # associate discourseme with analysis
    analysis.discoursemes.append(discourseme)
    db.session.add(analysis)
    db.session.commit()
    msg = 'associated discourseme %s with analysis %s' % (discourseme, analysis)
    log.debug(msg)

    return jsonify({'msg': msg}), 200


# DELETE
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/discourseme/<discourseme>/',
    methods=['DELETE']
)
@user_required
def delete_discourseme_from_analysis(username, analysis, discourseme):
    """ Remove discourseme from analysis.

    parameters:
      - name: username
        type: str
        description: username, links to user
      - name: analysis
        type: int
        description: analysis id
      - name: discourseme
        type: int
        description: discourseme id to remove
    responses:
      200:
         description: "deleted discourseme from analysis"
      404:
         description: "no such analysis"
         description: "no such discourseme"
         description: "discourseme not linked to analysis"

    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('no such analysis %s', analysis)
        return jsonify({'msg': 'no such analysis'}), 404

    # get discourseme
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        log.debug('no such discourseme %s', discourseme)
        return jsonify({'msg': 'no such discourseme'}), 404

    # check link
    analysis_discourseme = discourseme in analysis.discoursemes
    if not analysis_discourseme:
        log.warn('discourseme %s not linked to analysis %s', discourseme, analysis)
        return jsonify({'msg': 'discourseme not linked to analysis'}), 404

    # delete
    analysis.discoursemes.remove(discourseme)
    db.session.commit()

    log.debug('deleted discourseme %s from analysis %s', discourseme, analysis)
    return jsonify({'msg': 'deleted discourseme from analysis'}), 200


##############
# COLLOCATES #
##############

@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/collocate/',
    methods=['GET']
)
@user_required
def get_collocate_for_analysis(username, analysis):
    """ Get collocate table for analysis.

    parameters:
      - name: username
        description: username, links to user
      - name: analysis
        description: analysis id
      - name: window_size
        type: int
        description: window size
      - name: discourseme
        type: list
        required: False
        description: discourseme id(s) to include in constellation
      - name: collocate
        type: list
        required: False
        description: lose item(s) for additional discourseme to include
      - name: cut_off
        type: int
        description: how many collocates? [200]
      - name: order
        type: str
        description: how to sort them? (column in result table) [log_likelihood]

    responses:
      200:
        description: collocates
      400:
        description: "wrong request parameters"
      404:
        description: "empty result"
    """
    # TODO: rename collocate ./. items

    # get user
    user = User.query.filter_by(username=username).first()

    # check request
    # ... analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'empty result'}), 404
    # ... window size
    window_size = request.args.get('window_size', 3)
    try:
        window_size = int(window_size)
    except TypeError:
        log.debug('wrong type of window size')
        return jsonify({'msg': 'wrong request parameters'}), 400
    # ... optional discourseme ID list
    discourseme_ids = request.args.getlist('discourseme', None)
    # ... optional additional items
    items = [cqp_escape(i) for i in request.args.getlist('collocate', None)]

    # not set yet
    cut_off = request.args.get('cut_off', 200)
    order = request.args.get('order', 'log_likelihood')
    flags_query = "%cd"
    escape = False
    flags_show = ""
    min_freq = 2
    ams = request.args.get('ams', None)

    # pre-process request
    # ... floating discoursemes
    additional_discoursemes = dict()
    if items:
        # create discourseme for additional items on the fly
        additional_discoursemes['collocate'] = items
    if discourseme_ids:
        # get all discoursemes from database and append
        discoursemes = Discourseme.query.filter(
            Discourseme.id.in_(discourseme_ids), Discourseme.user_id == user.id
        ).all()
        for d in discoursemes:
            additional_discoursemes[str(d.id)] = d.items

    # use cwb-ccc to extract data
    collocates = ccc_collocates(
        corpus_name=analysis.corpus,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        topic_items=analysis.items,
        s_context=analysis.s_break,
        windows=[window_size],
        context=analysis.context,
        additional_discoursemes=additional_discoursemes,
        p_query=analysis.p_query,
        flags_query=flags_query,
        s_query=analysis.s_break,
        p_show=[analysis.p_analysis],
        flags_show=flags_show,
        ams=ams,
        cut_off=cut_off,
        min_freq=min_freq,
        order=order,
        escape=escape
    )[window_size]

    if collocates.empty:
        log.debug('no collocates available for window size %s', window_size)
        return jsonify({'msg': 'empty result'}), 404

    # post-process result
    df_json = collocates.to_json()
    return df_json, 200


#####################
# CONCORDANCE LINES #
#####################
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/concordance/',
    methods=['GET']
)
@user_required
def get_concordance_for_analysis(username, analysis):
    """ Get concordance lines for analysis.

    parameters:
      - name: username
        description: username, links to user
      - name: analysis
        description: analysis_id
      - name: window_size
        type: int
        description: window size for context
        default: 3
      - name: item
        type: list
        required: False
        description: lose item(s) for additional discourseme to include
      - name: cut_off
        type: int
        description: how many lines?
        default: 100
      - name: order
        type: str
        description: how to sort them? (column in result table)
        default: random
      - name: s_meta
        type: str
        description: what s-att-annotation to retrieve
        default: analysis.s_break
    responses:
      200:
        description: concordance
      400:
        description: "wrong request parameters"
      404:
        description: "empty result"
    """
    # TODO: rename item ./. items

    # get user
    user = User.query.filter_by(username=username).first()

    # check request
    # ... analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('no such analysis %s', analysis)
        return jsonify({'msg': 'empty result'}), 404
    # ... window size
    window_size = request.args.get('window_size', 3)
    try:
        window_size = int(window_size)
    except TypeError:
        log.debug('wrong type of window size')
        return jsonify({'msg': 'wrong request parameters'}), 400
    # ... optional discourseme ID list
    discourseme_ids = request.args.getlist('discourseme', None)
    # ... optional additional items
    items = [cqp_escape(i) for i in request.args.getlist('item', None)]
    # ... how many?
    cut_off = request.args.get('cut_off', 1000)
    # ... how to sort them?
    order = request.args.get('order', 'random')
    # ... where's the meta data?
    s_show = [i for i in request.args.getlist('s_meta', None)]

    # pre-process request
    # ... get associated topic discourseme
    topic_discourseme = Discourseme.query.filter_by(id=analysis.topic_id).first()
    # ... further discoursemes as a dict {name: items}
    additional_discoursemes = dict()
    if items:
        # create discourseme for additional items on the fly
        additional_discoursemes['collocate'] = items

    # for discourseme in analysis.discoursemes:
    #     additional_discoursemes[discourseme.name] = discourseme.items
    # get all discoursemes from database and append
    discoursemes = Discourseme.query.filter(
        Discourseme.id.in_(discourseme_ids), Discourseme.user_id == user.id
    ).all()
    for d in discoursemes:
        additional_discoursemes[str(d.id)] = d.items

    # pack p-attributes
    p_show = list(set(['word', analysis.p_query]))

    # use cwb-ccc to extract concordance lines
    concordance = ccc_concordance(
        corpus_name=analysis.corpus,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        topic_items=analysis.items,
        topic_name=topic_discourseme.name,
        s_context=analysis.s_break,
        window_size=window_size,
        context=analysis.context,
        additional_discoursemes=additional_discoursemes,
        p_query=analysis.p_query,
        p_show=p_show,
        s_show=s_show,
        s_query=analysis.s_break,
        order=order,
        cut_off=cut_off
    )

    if concordance is None:
        log.debug('no concordance available for analysis %s', analysis)
        return jsonify({'msg': 'empty result'}), 404

    conc_json = jsonify(concordance)

    return conc_json, 200


#######################
# FREQUENCY BREAKDOWN #
#######################
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/breakdown/',
    methods=['GET']
)
@user_required
def get_breakdown_for_analysis(username, analysis):
    """ Get concordance lines for analysis.

    parameters:
      - name: username
        description: username, links to user
      - name: analysis
        description: analysis_id
    responses:
      200:
        description: breakdown
      400:
        description: "wrong request parameters"
      404:
        description: "empty result"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # check request
    # ... analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('no such analysis %s', analysis)
        return jsonify({'msg': 'empty result'}), 404

    # pack p-attributes
    p_show = request.args.getlist('p_show', ['word'])

    # use cwb-ccc to extract concordance lines
    breakdown = ccc_breakdown(
        corpus_name=analysis.corpus,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        topic_items=analysis.items,
        p_query=analysis.p_query,
        p_show=p_show,
        s_query=analysis.s_break,
    )

    if breakdown is None:
        log.debug('no breakdown available for analysis %s', analysis)
        return jsonify({'msg': 'empty result'}), 404

    breakdown_json = jsonify(breakdown)

    return breakdown_json, 200
