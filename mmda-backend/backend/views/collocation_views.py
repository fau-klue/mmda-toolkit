#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Collocation view
"""

# requirements
from flask import Blueprint, request, jsonify, current_app
from flask_expects_json import expects_json
from ccc.utils import cqp_escape

# backend
from backend import db
from backend import user_required
# backend.analysis
from backend.analysis.validators import COLLOCATION_SCHEMA, UPDATE_SCHEMA
from backend.analysis.semspace import generate_semantic_space, generate_items_coordinates
from backend.analysis.ccc import ccc_concordance, ccc_collocates, ccc_breakdown
from backend.analysis.ccc import ccc_corpus, ccc_meta
# backend.models
from backend.models.user_models import User
from backend.models.collocation_models import Collocation
from backend.models.discourseme_models import Discourseme
from backend.models.coordinates_models import Coordinates

# logging
from logging import getLogger


collocation_blueprint = Blueprint('collocation', __name__, template_folder='templates')

log = getLogger('mmda-logger')


###############
# COLLOCATION #
###############

# CREATE
@collocation_blueprint.route('/api/user/<username>/collocation/', methods=['POST'])
@expects_json(COLLOCATION_SCHEMA)
@user_required
def create_collocation(username):
    """ Create new collocation analysis for given user.

    parameters:
      - name: username
        type: str

      - name: corpus
        type: str
        description: name of corpus in API
      - name: discourseme
        type: str or dict
        description: new discourseme (<str>) or existing discourseme (<dict>)
      - name: items
        type: list
        description: items to search for

      - name: p_query
        type: str
        description: p-attribute to query on [lemma]
      - name: p_collocation
        type: str
        description: p-attribute to use for collocates [lemma]
      - name: s_break
        type: str
        description: s-attribute to break context at [text]
      - name: context
        type: int
        description: context size in tokens
        default: 10

      - name: cut_off
        type: int
        description: how many collocates?
        default: 500
      - name: order
        type: str
        description: how to sort them? (column in result table) [log_likelihood]

    responses:
       201:
         description: collocation.id
       400:
         description: "wrong request parameters"
       404:
         description: "empty result"
    """

    user = User.query.filter_by(username=username).first()

    # PARAMETERS #
    # required
    corpus_name = request.json.get('corpus')
    discourseme = request.json.get('discourseme')
    items = request.json.get('items')

    # more or less reasonable defaults
    p_query = request.json.get('p_query', 'lemma')
    p_collocation = request.json.get('p_collocation', 'lemma')
    s_break = request.json.get('s_break', 'text')
    context = request.json.get('context', 10)

    # not set yet
    cut_off = request.json.get('cut_off', 500)
    order = request.json.get('order', 'log_likelihood')
    flags_query = request.json.get('flags_query', '%c')
    escape_query = request.json.get('escape', False)
    flags_show = request.args.get('flags_show', flags_query)
    min_freq = request.json.get('min_freq', 2)
    ams = request.json.get('ams', None)
    collocation_name = request.json.get('name', None)

    # translation
    p_show = [p_collocation]

    # VALIDATION
    # TODO check at least discourseme and items
    if corpus_name not in current_app.config['CORPORA']:
        msg = 'no corpus "%s"', corpus_name
        log.debug(msg)
        return jsonify({'msg': msg}), 400

    # PROCESS
    # generate collocate tables: dict of dataframes with key == window_size
    # == [item] O11 .. E22 AMs .. ==
    log.debug('starting collocation analysis')
    breakdown, collocates = ccc_collocates(
        corpus_name=corpus_name,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        topic_items=items,
        s_context=s_break,
        windows=range(1, context + 1),
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
        escape=escape_query
    )

    # no query matches?
    if collocates is None:
        return jsonify({'msg': "no query matches"}), 404

    # get tokens for coordinate generation
    # TODO: re-implement in backend
    log.debug('generating semantic space')
    tokens = []
    for df in collocates.values():
        tokens.extend(df.index)
    tokens = list(set(tokens))
    log.debug('extracted %d tokens for collocation semantic space' % len(tokens))

    # no collocates?
    if len(tokens) == 0:
        log.debug('no collocates found for %s', items)
        return jsonify({'msg': 'empty result'}), 404

    # generate coordinates
    # dataframe == [token] x y x_user y_user ==
    semantic_space = generate_semantic_space(tokens, current_app.config['CORPORA'][corpus_name]['embeddings'])

    # DISCOURSEME MANAGEMENT
    if isinstance(discourseme, str):
        # create new discourseme
        topic_discourseme = Discourseme(name=discourseme, items=items, user_id=user.id)
        db.session.add(topic_discourseme)
        db.session.commit()
        log.debug('created discourseme %s', topic_discourseme.id)
    elif isinstance(discourseme, dict):
        # retrieve chosen discourseme
        topic_discourseme = Discourseme.query.filter_by(id=discourseme['id']).first()
    else:
        msg = "discourseme of type %s" % str(type(discourseme))
        log.debug(msg)
        return jsonify({'msg': msg}), 400

    # SAVE TO DATABASE
    # analysis
    collocation = Collocation(
        name=collocation_name,
        corpus=corpus_name,
        p_query=p_query,
        flags_query=flags_query,
        escape_query=escape_query,
        p_collocation=p_collocation,
        s_break=s_break,
        context=context,
        items=items,
        topic_id=topic_discourseme.id,
        user_id=user.id,
    )
    db.session.add(collocation)
    db.session.commit()
    log.debug('added collocation %s to db', collocation.id)

    # semantic space
    coordinates = Coordinates(collocation_id=collocation.id, data=semantic_space)
    db.session.add(coordinates)
    db.session.commit()
    log.debug('added coordinates %s to db', coordinates.id)

    return jsonify({'msg': collocation.id}), 201


# READ ALL
@collocation_blueprint.route('/api/user/<username>/collocation/', methods=['GET'])
@user_required
def get_all_collocation(username):
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

    collocation_analyses = Collocation.query.filter_by(user_id=user.id).all()
    collocation_list = [collocation.serialize for collocation in collocation_analyses]

    return jsonify(collocation_list), 200


# READ
@collocation_blueprint.route('/api/user/<username>/collocation/<collocation>/', methods=['GET'])
@user_required
def get_collocation(username, collocation):
    """ Get details of collocation analysis.

    parameters:
      - username: username
        type: str
        description: username, links to user
      - name: collocation
        type: str
        description: collocation id
    responses:
       200:
         description: dict of collocation analysis details
       404:
         description: "no such analysis"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    analysis = Collocation.query.filter_by(id=collocation, user_id=user.id).first()
    if not analysis:
        log.debug('no such analysis %s', analysis)
        return jsonify({'msg': 'no such analysis'}), 404

    return jsonify(analysis.serialize), 200


# UPDATE
@collocation_blueprint.route('/api/user/<username>/collocation/<collocation>/', methods=['PUT'])
@expects_json(UPDATE_SCHEMA)
@user_required
def update_collocation(username, collocation):
    """ Edit analysis. Only the name can be updated. Deprecated.

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
        log.debug('no name provided for analysis %s', collocation)
        return jsonify({'msg': 'wrong request parameters'}), 400

    # update analysis
    analysis = Collocation.query.filter_by(id=collocation, user_id=user.id).first()
    analysis.name = name
    db.session.commit()

    log.debug('updated analysis with ID %s', analysis)
    return jsonify({'msg': analysis.id}), 200


# DELETE
@collocation_blueprint.route('/api/user/<username>/collocation/<collocation>/', methods=['DELETE'])
@user_required
def delete_collocation(username, collocation):
    """ Delete collocation.

    parameters:
      - username: username
        type: str
        description: username, links to user
      - name: collocation
        type: str
        description: collocation id
    responses:
       200:
         description: "deleted"
       404:
         description: "no such collocation"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # delete collocation
    collocation = Collocation.query.filter_by(id=collocation, user_id=user.id).first()
    if not collocation:
        log.debug('no such collocation %s', collocation)
        return jsonify({'msg': 'no such collocation'}), 404

    db.session.delete(collocation)
    db.session.commit()

    log.debug('deleted collocation with ID %s', collocation)
    return jsonify({'msg': 'deleted'}), 200


###########################
# ASSOCIATED DISCOURSEMES #
###########################

# READ
@collocation_blueprint.route('/api/user/<username>/collocation/<collocation>/discourseme/', methods=['GET'])
@user_required
def get_discoursemes_for_collocation(username, collocation):
    """ Return list of discoursemes for collocation.

    parameters:
      - username: username
        type: str
        description: username, links to user
      - name: collocation
        type: str
        description: collocation id
    responses:
       200:
         description: list of associated discoursemes
       404:
         description: "no such collocation"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get collocation
    collocation = Collocation.query.filter_by(id=collocation, user_id=user.id).first()
    if not collocation:
        log.debug('no such analysis %s', collocation)
        return jsonify({'msg': 'no such analysis'}), 404

    # get discoursemes as list
    collocation_discoursemes = [
        discourseme.serialize for discourseme in collocation.discoursemes
    ]
    if not collocation_discoursemes:
        log.debug('no disoursemes associated')
        return jsonify([]), 200

    return jsonify(collocation_discoursemes), 200


# UPDATE
@collocation_blueprint.route('/api/user/<username>/collocation/<collocation>/discourseme/<discourseme>/', methods=['PUT'])
@user_required
def put_discourseme_into_collocation(username, collocation, discourseme):
    """ Associate a discourseme with collocation.

    parameters:
      - name: username
        type: str
        description: username, links to user
      - name: collocation
        type: int
        description: collocation id
      - name: discourseme
        type: int
        description: discourseme id to associate
    responses:
      200:
         description: "already linked"
         description: "updated"
      404:
         description: "no such collocation"
         description: "no such discourseme"
      409:
         description: "discourseme is already topic of collocation"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get collocation analysis
    collocation = Collocation.query.filter_by(id=collocation, user_id=user.id).first()
    if not collocation:
        msg = 'no such collocation %s' % collocation
        log.debug(msg)
        return jsonify({'msg': msg}), 404

    # get discourseme
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        msg = 'no such discourseme %s' % discourseme
        log.debug(msg)
        return jsonify({'msg': msg}), 404

    # check if discourseme already associated or already topic of collocation analysis
    collocation_discourseme = discourseme in collocation.discoursemes
    is_own_topic_discourseme = discourseme.id == collocation.topic_id
    if is_own_topic_discourseme:
        msg = 'discourseme %s is already topic of the collocation analysis', discourseme
        log.debug(msg)
        return jsonify({'msg': msg}), 409
    if collocation_discourseme:
        msg = 'discourseme %s is already associated', discourseme
        log.debug(msg)
        return jsonify({'msg': msg}), 200

    corpus_name = collocation.corpus
    items = collocation.items
    s_break = collocation.s_break
    p_query = collocation.p_query
    flags_query = collocation.flags_query
    escape_query = collocation.escape_query
    context = collocation.context
    ams = None

    flags_show = collocation.flags_query
    p_show = [collocation.p_query]
    cut_off = 200
    order = 'log_likelihood'
    min_freq = 1

    # create new analysis (see below for alternative)
    breakdown, collocates = ccc_collocates(
        corpus_name=corpus_name,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        topic_items=items,
        s_context=s_break,
        windows=[context],
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
        escape=escape_query
    )

    # ALTERNATIVE POST-HOC UPDATE
    # check if discourseme already associated with corpus
    # i.e. there is at least one collocation analysis of this discourseme in this corpus
    # new_items = breakdown.loc[breakdown['discourseme'] != 'topic'].index
    # 1) generate new coordinates for new_items
    # 2) remove items (incl. MWUs) in discoursemes from collocate table / semcloud
    # tokens = set(discourseme.items)
    # coordinates = Coordinates.query.filter_by(collocation_id=collocation.id).first()
    # semantic_space = coordinates.data
    # diff = tokens - set(semantic_space.index)
    # if len(diff) > 0:
    #     log.debug("generating additional coordinates for %d items" % len(diff))
    #     new_coordinates = generate_items_coordinates(
    #         diff,
    #         semantic_space,
    #         current_app.config['CORPORA'][collocation.corpus]['embeddings']
    #     )
    #     if not new_coordinates.empty:
    #         log.debug('appending new coordinates to semantic space')
    #         semantic_space.append(new_coordinates, sort=True)
    #         coordinates.data = semantic_space
    #         db.session.commit()

    # update database
    collocation.discoursemes.append(discourseme)
    db.session.add(collocation)
    db.session.commit()
    msg = 'associated discourseme %s with collocation analysis %s' % (discourseme, collocation)
    log.debug(msg)

    return jsonify({'msg': msg}), 200


# DELETE
@collocation_blueprint.route('/api/user/<username>/collocation/<collocation>/discourseme/<discourseme>/', methods=['DELETE'])
@user_required
def delete_discourseme_from_collocation(username, collocation, discourseme):
    """ Remove discourseme from collocation.

    parameters:
      - name: username
        type: str
        description: username, links to user
      - name: collocation
        type: int
        description: collocation id
      - name: discourseme
        type: int
        description: discourseme id to remove
    responses:
      200:
         description: "deleted discourseme from collocation"
      404:
         description: "no such analysis"
         description: "no such discourseme"
         description: "discourseme not linked to collocation"

    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get collocation
    collocation = Collocation.query.filter_by(id=collocation, user_id=user.id).first()
    if not collocation:
        log.debug('no such collocation %s', collocation)
        return jsonify({'msg': 'no such analysis'}), 404

    # get discourseme
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        log.debug('no such discourseme %s', discourseme)
        return jsonify({'msg': 'no such discourseme'}), 404

    # check link
    collocation_discourseme = discourseme in collocation.discoursemes
    if not collocation_discourseme:
        log.warn('discourseme %s not linked to collocation analysis %s', discourseme, collocation)
        return jsonify({'msg': 'discourseme not linked to analysis'}), 404

    # TODO re-do collocation analysis

    # delete
    collocation.discoursemes.remove(discourseme)
    db.session.commit()

    log.debug('deleted discourseme %s from collocation analysis %s', discourseme, collocation)
    return jsonify({'msg': 'deleted discourseme from collocation analysis'}), 200


##############
# COLLOCATES #
##############

@collocation_blueprint.route('/api/user/<username>/collocation/<collocation>/collocate/', methods=['GET'])
@user_required
def get_collocate_for_collocation(username, collocation):
    """ Get collocate table for collocation analysis.

    parameters:
      - name: username
        description: username, links to user
      - name: collocation
        description: collocation id

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
        description: lose item(s) for ad-hoc discourseme to include

      - name: cut_off
        type: int
        description: how many collocates?
        default: 500
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

    user = User.query.filter_by(username=username).first()
    collocation = Collocation.query.filter_by(id=collocation, user_id=user.id).first()

    # PARAMETERS #
    # required
    window_size = int(request.args.get('window_size'))

    # optional
    # ... optional discourseme ID list
    discourseme_ids = request.args.getlist('discourseme', None)
    # ... optional additional items
    items = request.args.getlist('collocate', None)

    # not set yet
    cut_off = request.args.get('cut_off', 500)
    order = request.args.get('order', 'log_likelihood')
    flags_show = request.args.get('flags_show', collocation.flags_query)
    min_freq = request.args.get('min_freq', 2)
    ams = request.args.get('ams', None)

    # VALIDATION
    if not collocation:
        msg = 'No such collocation %s' % collocation
        log.debug(msg)
        return jsonify({'msg': msg}), 404

    # pre-process request
    # ... filter for SOC
    filter_discoursemes = dict()
    if discourseme_ids:
        discoursemes = Discourseme.query.filter(
            Discourseme.id.in_(discourseme_ids), Discourseme.user_id == user.id
        ).all()
        for d in discoursemes:
            filter_discoursemes[str(d.id)] = d.items

    # ... floating discoursemes
    additional_discoursemes = dict()
    if items:
        # create discourseme for additional items on the fly
        additional_discoursemes['collocate'] = [cqp_escape(i) for i in items]

    # ... highlight associated discoursemes
    for d in collocation.discoursemes:
        additional_discoursemes[str(d.id)] = d.items

    # get collocates: dict of dataframes with key == window_size
    # collocates, topic_breakdown, discoursemes_breakdown =
    breakdown, collocates = ccc_collocates(
        corpus_name=collocation.corpus,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        topic_items=collocation.items,
        s_context=collocation.s_break,
        windows=[window_size],
        context=collocation.context,
        additional_discoursemes=additional_discoursemes,
        filter_discoursemes=filter_discoursemes,
        p_query=collocation.p_query,
        flags_query=collocation.flags_query,
        s_query=collocation.s_break,
        p_show=[collocation.p_collocation],
        flags_show=flags_show,
        ams=ams,
        cut_off=cut_off,
        min_freq=min_freq,
        order=order,
        escape=collocation.escape_query
    )
    collocates = collocates[window_size]

    # TODO:
    # all items of associated discoursemes
    # breakdown.loc[breakdown['discourseme'] != 'topic']
    # have to be included in the map

    if collocates.empty:
        log.debug('no collocates available for window size %s', window_size)
        return jsonify({'msg': 'empty result'}), 404

    # MAKE SURE THERE ARE COORDINATES FOR ALL TOKENS
    tokens = set(collocates.index)
    coordinates = Coordinates.query.filter_by(collocation_id=collocation.id).first()
    semantic_space = coordinates.data

    diff = tokens - set(semantic_space.index)
    if len(diff) > 0:
        log.debug("generating additional coordinates for %d items" % len(diff))
        new_coordinates = generate_items_coordinates(
            diff,
            semantic_space,
            current_app.config['CORPORA'][collocation.corpus]['embeddings']
        )
        if not new_coordinates.empty:
            log.debug('appending new coordinates to semantic space')
            semantic_space = semantic_space.append(new_coordinates, sort=True)
            coordinates.data = semantic_space
            db.session.commit()

    # post-process result
    df_json = collocates.to_json()

    return df_json, 200


#####################
# CONCORDANCE LINES #
#####################
@collocation_blueprint.route('/api/user/<username>/collocation/<collocation>/concordance/', methods=['GET'])
@user_required
def get_concordance_for_collocation(username, collocation):
    """ Get concordance lines for collocation.

    parameters:
      - name: username
        description: username, links to user
      - name: collocation
        description: collocation_id
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
        default: 1000
      - name: order
        type: str
        description: how to sort them? (column in result table)
        default: random
      - name: s_meta
        type: str
        description: what s-att-annotation to retrieve
        default: collocation.s_break
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
    # ... collocation
    collocation = Collocation.query.filter_by(id=collocation, user_id=user.id).first()
    if not collocation:
        log.debug('no such collocation %s', collocation)
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
    corpus = ccc_corpus(collocation.corpus,
                        cqp_bin=current_app.config['CCC_CQP_BIN'],
                        registry_path=current_app.config['CCC_REGISTRY_PATH'],
                        data_path=current_app.config['CCC_DATA_PATH'])
    # s_show = [i for i in request.args.getlist('s_meta', None)]
    s_show = corpus['s-annotations']

    # pack p-attributes
    p_show = list(set(['word', collocation.p_query]))

    # pre-process request
    # ... get associated topic discourseme (no need if not interested in name)
    # topic_discourseme = Discourseme.query.filter_by(id=collocation.topic_id).first()
    # ... further discoursemes as a dict {name: items}
    filter_discoursemes = dict()
    if items:
        # create discourseme for additional items on the fly
        filter_discoursemes['collocate'] = items

    # SOC
    if discourseme_ids:
        discoursemes = Discourseme.query.filter(
            Discourseme.id.in_(discourseme_ids), Discourseme.user_id == user.id
        ).all()
        for d in discoursemes:
            filter_discoursemes[str(d.id)] = d.items

    additional_discoursemes = dict()
    for d in collocation.discoursemes:
        additional_discoursemes[str(d.id)] = d.items

    random_seed = 42

    # use cwb-ccc to extract concordance lines
    concordance = ccc_concordance(
        corpus_name=collocation.corpus,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        topic_discourseme={'topic': collocation.items},
        filter_discoursemes=filter_discoursemes,
        additional_discoursemes=additional_discoursemes,
        s_context=collocation.s_break,
        window_size=window_size,
        context=None,
        p_query=collocation.p_query,
        p_show=p_show,
        s_show=s_show,
        s_query=collocation.s_break,
        order=order,
        cut_off=cut_off,
        flags_query=collocation.flags_query,
        escape_query=collocation.escape_query,
        random_seed=random_seed
    )

    if concordance is None:
        log.debug('no concordance available for collocation %s', collocation)
        return jsonify({'msg': 'empty result'}), 404

    conc_json = jsonify(concordance)

    return conc_json, 200


#######################
# FREQUENCY BREAKDOWN #
#######################
@collocation_blueprint.route('/api/user/<username>/collocation/<collocation>/breakdown/', methods=['GET'])
@user_required
def get_breakdown_for_collocation(username, collocation):
    """ Get concordance lines for collocation.

    parameters:
      - name: username
        description: username, links to user
      - name: collocation
        description: collocation_id
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
    # ... collocation
    collocation = Collocation.query.filter_by(id=collocation, user_id=user.id).first()
    if not collocation:
        log.debug('no such collocation %s', collocation)
        return jsonify({'msg': 'empty result'}), 404

    flags_show = request.args.get('flags_show', collocation.flags_query)

    # use cwb-ccc to extract concordance lines
    breakdown = ccc_breakdown(
        corpus_name=collocation.corpus,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        topic_items=collocation.items,
        p_query=collocation.p_query,
        p_show=[collocation.p_collocation],
        s_query=collocation.s_break,
        flags_query=collocation.flags_query,
        escape=collocation.escape_query,
        flags_show=flags_show
    )

    if breakdown is None:
        log.debug('no breakdown available for collocation %s', collocation)
        return jsonify({'msg': 'empty result'}), 404

    breakdown_json = jsonify(breakdown)

    return breakdown_json, 200


#####################
# META DISTRIBUTION #
#####################
@collocation_blueprint.route('/api/user/<username>/collocation/<collocation>/meta/', methods=['GET'])
@user_required
def get_meta_for_collocation(username, collocation):
    """ Get concordance lines for collocation.

    parameters:
      - name: username
        description: username, links to user
      - name: collocation
        description: collocation_id
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
    # ... collocation
    collocation = Collocation.query.filter_by(id=collocation, user_id=user.id).first()
    if not collocation:
        log.debug('no such collocation %s', collocation)
        return jsonify({'msg': 'empty result'}), 404

    # pack p-attributes
    # ... where's the meta data?
    corpus = ccc_corpus(collocation.corpus,
                        cqp_bin=current_app.config['CCC_CQP_BIN'],
                        registry_path=current_app.config['CCC_REGISTRY_PATH'],
                        data_path=current_app.config['CCC_DATA_PATH'])
    # s_show = [i for i in request.args.getlist('s_meta', None)]
    s_show = corpus['s-annotations']

    # use cwb-ccc to extract concordance lines
    meta = ccc_meta(
        corpus_name=collocation.corpus,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        topic_items=collocation.items,
        p_query=collocation.p_query,
        s_query=collocation.s_break,
        flags_query=collocation.flags_query,
        s_show=s_show,
        escape=collocation.escape_query
    )

    if meta is None:
        log.debug('no meta data available for collocation %s', collocation)
        return jsonify({'msg': 'empty result'}), 404

    meta_json = jsonify(meta)

    return meta_json, 200
