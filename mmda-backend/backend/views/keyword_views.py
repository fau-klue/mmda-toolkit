#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Keywords view
"""

# requirements
from flask import Blueprint, request, jsonify, current_app
# from flask_expects_json import expects_json
from ccc.utils import cqp_escape

# backend
from backend import db
from backend import user_required
# backend.analysis
# from backend.analysis.validators import ANALYSIS_SCHEMA, UPDATE_SCHEMA
from backend.analysis.semspace import generate_semantic_space, generate_items_coordinates
from backend.analysis.ccc import ccc_keywords, ccc_concordance, ccc_corpus
# backend.models
from backend.models.user_models import User
from backend.models.keyword_models import Keyword
from backend.models.discourseme_models import Discourseme
from backend.models.coordinates_models import Coordinates

# logging
from logging import getLogger


keyword_blueprint = Blueprint('keyword', __name__, template_folder='templates')

log = getLogger('mmda-logger')


####################
# KEYWORD ANALYSES #
####################

# CREATE
@keyword_blueprint.route('/api/user/<username>/keyword/', methods=['POST'])
# TODO @expects_json(ANALYSIS_SCHEMA)
@user_required
def create_keyword(username):
    """ Create new keyword analysis for given user.

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

      - name: s_break
        type: str
        description: where to limit concordance lines

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
    flags = request.json.get('flags', '%c')
    flags_reference = request.json.get('flags_reference', '%c')
    s_break = request.json.get('s_break', 's')

    keyword_analysis_name = request.json.get('name', None)

    # VALIDATION
    for c in [corpus, corpus_reference]:
        if corpus not in current_app.config['CORPORA']:
            msg = 'no corpus "%s"' % c
            log.debug(msg)
            return jsonify({'msg': msg}), 400
    # TODO check attributes

    # PROCESS
    log.debug('starting keyword analysis')
    keywords = ccc_keywords(
        corpus=corpus,
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
    tokens = list(set(keywords.index))
    log.debug('extracted %d tokens for keyword semantic space' % len(tokens))

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
    keyword_analysis = Keyword(
        name=keyword_analysis_name,
        corpus=corpus,
        corpus_reference=corpus_reference,
        p=p,
        p_reference=p_reference,
        s_break=s_break,
        flags=flags,
        flags_reference=flags_reference,
        user_id=user.id
    )

    db.session.add(keyword_analysis)
    db.session.commit()
    log.debug('added keyword analysis %s to db', keyword_analysis.id)

    # semantic space
    coordinates = Coordinates(
        keyword_id=keyword_analysis.id,
        data=semantic_space
    )
    db.session.add(coordinates)
    db.session.commit()
    log.debug('added coordinates %s to db', coordinates.id)

    return jsonify({'msg': keyword_analysis.id}), 201


# READ ALL
@keyword_blueprint.route('/api/user/<username>/keyword/', methods=['GET'])
@user_required
def get_all_keywords(username):
    """ List all keyword analyses for given user.

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

    keywords = Keyword.query.filter_by(user_id=user.id).all()
    keyword_list = [kw.serialize for kw in keywords]

    return jsonify(keyword_list), 200


# READ
@keyword_blueprint.route('/api/user/<username>/keyword/<keyword>/', methods=['GET'])
@user_required
def get_keyword(username, keyword):
    """ Get details of keyword analysis.

    parameters:
      - username: username
        type: str
        description: username, links to user
      - name: keyword_id
        type: str
        description: keyword id
    responses:
       200:
         description: dict of keyword details
       404:
         description: "no such analysis"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    keyword = Keyword.query.filter_by(id=keyword, user_id=user.id).first()
    if not keyword:
        log.debug('no such keyword analysis %s', keyword)
        return jsonify({'msg': 'no such keyword analysis'}), 404

    return jsonify(keyword.serialize), 200


# DELETE
@keyword_blueprint.route('/api/user/<username>/keyword/<keyword>/', methods=['DELETE'])
@user_required
def delete_keyword(username, keyword):
    """ Delete keyword analysis.

    parameters:
      - username: username
        type: str
        description: username, links to user
      - name: keyword
        type: str
        description: keyword analysis id
    responses:
       200:
         description: "deleted"
       404:
         description: "no such keyword analysis"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # delete analysis
    keyword = Keyword.query.filter_by(id=keyword, user_id=user.id).first()
    if not keyword:
        log.debug('no such keyword analysis %s', keyword)
        return jsonify({'msg': 'no such keyword analysis'}), 404

    db.session.delete(keyword)
    db.session.commit()

    log.debug('deleted keyword analysis with ID %s', keyword)
    return jsonify({'msg': 'deleted'}), 200


###########################
# ASSOCIATED DISCOURSEMES #
###########################

# READ
@keyword_blueprint.route('/api/user/<username>/keyword/<keyword>/discourseme/', methods=['GET'])
@user_required
def get_discoursemes_for_keyword(username, keyword):
    """ Return list of discoursemes for keyword analysis.

    parameters:
      - username: username
        type: str
        description: username, links to user
      - name: keyword
        type: str
        description: keyword analysis id
    responses:
       200:
         description: list of associated discoursemes
       404:
         description: "no such keyword analysis"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    keyword = Keyword.query.filter_by(id=keyword, user_id=user.id).first()
    if not keyword:
        log.debug('no such keyword analysis %s', keyword)
        return jsonify({'msg': 'no such keyword analysis'}), 404

    # get discoursemes as list
    keyword_discoursemes = [
        discourseme.serialize for discourseme in keyword.discoursemes
    ]
    if not keyword_discoursemes:
        log.debug('no disoursemes associated')
        return jsonify([]), 200

    return jsonify(keyword_discoursemes), 200


# UPDATE
@keyword_blueprint.route('/api/user/<username>/keyword/<keyword>/discourseme/<discourseme>/', methods=['PUT'])
@user_required
def put_discourseme_into_keyword(username, keyword, discourseme):
    """ Associate a discourseme with keyword analysis.

    parameters:
      - name: username
        type: str
        description: username, links to user
      - name: keyword
        type: int
        description: keyword analysis id
      - name: discourseme
        type: int
        description: discourseme id to associate
    responses:
      200:
         description: "already linked"
         description: "updated"
      404:
         description: "no such keyword analysis"
         description: "no such discourseme"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    keyword = Keyword.query.filter_by(id=keyword, user_id=user.id).first()
    if not keyword:
        msg = 'no such keyword analysis %s' % keyword
        log.debug(msg)
        return jsonify({'msg': msg}), 404

    # get discourseme
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        msg = 'no such discourseme %s' % discourseme
        log.debug(msg)
        return jsonify({'msg': msg}), 404

    # check if discourseme already associated or already topic of analysis
    keyword_discourseme = discourseme in keyword.discoursemes
    if keyword_discourseme:
        msg = 'discourseme %s is already associated', discourseme
        log.debug(msg)
        return jsonify({'msg': msg}), 200

    # associate discourseme with analysis
    keyword.discoursemes.append(discourseme)
    db.session.add(keyword)
    db.session.commit()
    msg = 'associated discourseme %s with keyword analysis %s' % (discourseme, keyword)
    log.debug(msg)

    # update semantic space: add discourseme items
    tokens = set(discourseme.items)
    coordinates = Coordinates.query.filter_by(keyword_id=keyword.id).first()
    semantic_space = coordinates.data
    diff = tokens - set(semantic_space.index)
    if len(diff) > 0:
        log.debug("generating additional coordinates for %d items" % len(diff))
        new_coordinates = generate_items_coordinates(
            diff,
            semantic_space,
            current_app.config['CORPORA'][keyword.corpus]['embeddings']
        )
        if not new_coordinates.empty:
            log.debug('appending new coordinates to semantic space')
            semantic_space.append(new_coordinates, sort=True)
            coordinates.data = semantic_space
            db.session.commit()

    return jsonify({'msg': msg}), 200


# DELETE
@keyword_blueprint.route('/api/user/<username>/keyword/<keyword>/discourseme/<discourseme>/', methods=['DELETE'])
@user_required
def delete_discourseme_from_keyword(username, keyword, discourseme):
    """ Remove discourseme from keyword analysis.

    parameters:
      - name: username
        type: str
        description: username, links to user
      - name: keyword
        type: int
        description: keyword analysis id
      - name: discourseme
        type: int
        description: discourseme id to remove
    responses:
      200:
         description: "deleted discourseme from keyword analysis"
      404:
         description: "no such keyword analysis"
         description: "no such discourseme"
         description: "discourseme not linked to keyword analysis"

    """

    # get user
    user = User.query.filter_by(username=username).first()

    # get analysis
    keyword = Keyword.query.filter_by(id=keyword, user_id=user.id).first()
    if not keyword:
        log.debug('no such keyword analysis %s', keyword)
        return jsonify({'msg': 'no such keyword analysis'}), 404

    # get discourseme
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        log.debug('no such discourseme %s', discourseme)
        return jsonify({'msg': 'no such discourseme'}), 404

    # check link
    keyword_discourseme = discourseme in keyword.discoursemes
    if not keyword_discourseme:
        log.warn('discourseme %s not linked to keyword analysis %s', discourseme, keyword)
        return jsonify({'msg': 'discourseme not linked to keyword analysis'}), 404

    # delete
    keyword.discoursemes.remove(discourseme)
    db.session.commit()

    log.debug('deleted discourseme %s from keyword analysis %s', discourseme, keyword)
    return jsonify({'msg': 'deleted discourseme from keyword analysis'}), 200


############
# KEYWORDS #
############

@keyword_blueprint.route('/api/user/<username>/keyword/<keyword>/keywords/', methods=['GET'])
@user_required
def get_keywords_for_keyword(username, keyword):
    """ Get keywords table for keyword analysis.

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
    keyword = Keyword.query.filter_by(id=keyword, user_id=user.id).first()

    corpus = keyword.corpus
    corpus_reference = keyword.corpus_reference
    p = keyword.p
    p_reference = keyword.p_reference

    # not set yet
    min_freq = 2
    cut_off = 500
    order = 'log_likelihood'
    flags_show = keyword.flags
    # min_freq = request.json.get('min_freq', 2)
    # cut_off = request.args.get('cut_off', 500)
    # order = request.args.get('order', 'log_likelihood')
    # flags = request.args.get('flags', '')
    # flags_reference = request.args.get('flags', '')

    # VALIDATION
    if not keyword:
        msg = 'No such keyword analysis %s' % keyword
        log.debug(msg)
        return jsonify({'msg': msg}), 404

    log.debug('starting keyword analysis')
    keywords = ccc_keywords(
        corpus=corpus,
        corpus_reference=corpus_reference,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        p=p,
        p_reference=p_reference,
        flags=keyword.flags,
        flags_reference=keyword.flags_reference,
        order=order,
        cut_off=cut_off,
        min_freq=min_freq,
        flags_show=flags_show
    )

    if keywords.empty:
        log.debug('no keywords available')
        return jsonify({'msg': 'empty result'}), 404

    # MAKE SURE THERE ARE COORDINATES FOR ALL TOKENS
    tokens = set(keywords.index)
    coordinates = Coordinates.query.filter_by(keyword_id=keyword.id).first()
    semantic_space = coordinates.data
    diff = tokens - set(semantic_space.index)
    if len(diff) > 0:
        log.debug("generating additional coordinates for %d items" % len(diff))
        new_coordinates = generate_items_coordinates(
            diff,
            semantic_space,
            current_app.config['CORPORA'][keyword.corpus]['embeddings']
        )
        if not new_coordinates.empty:
            log.debug('appending new coordinates to semantic space')
            semantic_space = semantic_space.append(new_coordinates, sort=True)
            coordinates.data = semantic_space
            db.session.commit()

    # post-process result
    df_json = keywords.to_json()

    return df_json, 200


#####################
# CONCORDANCE LINES #
#####################
@keyword_blueprint.route('/api/user/<username>/keyword/<keyword>/concordance/', methods=['GET'])
@user_required
def get_concordance_for_keyword(username, keyword):
    """ Get concordance lines for analysis.

    parameters:
      - name: username
        description: username, links to user
      - name: keyword
        description: keyword_analysis_id
      - name: item
        type: str
        description: item to get lines for
      - name: cut_off
        type: int
        description: how many lines?
        default: 1000
      - name: order
        type: str
        description: how to sort them? (column in result table)
        default: random
    responses:
      200:
        description: concordance
      400:
        description: "wrong request parameters"
      404:
        description: "empty result"
    """

    # get user
    user = User.query.filter_by(username=username).first()

    # check request
    # ... analysis
    keyword = Keyword.query.filter_by(id=keyword, user_id=user.id).first()
    if not keyword:
        log.debug('no such keyword analysis %s', keyword)
        return jsonify({'msg': 'empty result'}), 404
    # ... item to get concordance lines for
    item = request.args.get('item')
    if not item:
        return {}, 200
    item = cqp_escape(item)

    # ... highlight associated discoursemes
    additional_discoursemes = dict()
    for d in keyword.discoursemes:
        additional_discoursemes[str(d.id)] = d.items

    # ... how many?
    cut_off = request.args.get('cut_off', 1000)
    # ... how to sort them?
    order = request.args.get('order', 'random')
    # ... where's the meta data?
    corpus = ccc_corpus(keyword.corpus,
                        cqp_bin=current_app.config['CCC_CQP_BIN'],
                        registry_path=current_app.config['CCC_REGISTRY_PATH'],
                        data_path=current_app.config['CCC_DATA_PATH'])
    # s_show = [i for i in request.args.getlist('s_meta', None)]
    s_show = corpus['s-annotations']

    # pack p-attributes
    p_show = list(set(['word', keyword.p]))

    window_size = request.args.get('window_size', 50)
    s_break = keyword.s_break
    topic_discourseme = {'topic': [item]}
    filter_discoursemes = {}
    flags_query = "%c"
    escape_query = True
    random_seed = 42

    # use cwb-ccc to extract concordance lines
    concordance = ccc_concordance(
        corpus_name=keyword.corpus,
        cqp_bin=current_app.config['CCC_CQP_BIN'],
        registry_path=current_app.config['CCC_REGISTRY_PATH'],
        data_path=current_app.config['CCC_DATA_PATH'],
        lib_path=current_app.config['CCC_LIB_PATH'],
        topic_discourseme=topic_discourseme,
        filter_discoursemes=filter_discoursemes,
        additional_discoursemes=additional_discoursemes,
        s_context=s_break,
        window_size=window_size,
        context=None,
        p_query=keyword.p,
        p_show=p_show,
        s_show=s_show,
        s_query=s_break,
        order=order,
        cut_off=cut_off,
        flags_query=flags_query,
        escape_query=escape_query,
        random_seed=random_seed
    )

    if concordance is None:
        log.debug('no concordance available for analysis %s', keyword)
        return jsonify({'msg': 'empty result'}), 404

    conc_json = jsonify(concordance)

    return conc_json, 200
