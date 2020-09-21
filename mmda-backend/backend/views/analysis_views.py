"""
Analysis view
"""


# flask
from flask import Blueprint, request, jsonify, current_app
from flask_expects_json import expects_json
# backend
from backend import db
from backend import user_required
# backend.analysis
from backend.analysis.validators import ANALYSIS_SCHEMA, UPDATE_SCHEMA
from backend.analysis.tsne import (
    generate_semantic_space, generate_discourseme_coordinates
)
from backend.analysis.ccc import get_concordance, get_collocates
# backend.models
from backend.models.user_models import User
from backend.models.analysis_models import (
    Analysis, AnalysisDiscoursemes, Discourseme, Coordinates
)
# logging
from logging import getLogger

analysis_blueprint = Blueprint(
    'analysis', __name__,
    template_folder='templates'
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
    """
    Create a new analysis for given user

    parameters:
      - name: username
        description: username, links to user
      - name: name
        description: analysis name
      - name: corpus_name
        description: name of corpus
      - name: window_size
        type: int
        description: (maximum) context
      - name: p_query
        type: str
        description: p-attribute to query on [lemma]
      - name: s_break
        type: str
        description: s_context
      - name: items
        type: list
        required: False
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
         description: Error: Wrong request parameters
       404:
         description: Error: Empty result
    """

    # Check Request
    name = request.json.get('name', None)
    corpus_name = request.json.get('corpus', None)
    max_window_size = request.json.get('window_size', 3)
    p_query = request.json.get('p_query', 'lemma')
    s_break = request.json.get('s_break', None)
    items = request.json.get('items', [])
    cut_off = request.args.get('cut_off', 200)
    order = request.args.get('order', 'log_likelihood')

    # Check corpus
    if corpus_name not in current_app.config['CORPORA']:
        log.debug('No such corpus "%s"', corpus_name)
        return jsonify({'msg': 'Wrong request parameters'}), 400

    # Get User
    user = User.query.filter_by(username=username).first()

    # Add topic discourseme to DB
    topic_discourseme = Discourseme(
        name=name,
        items=items,
        user_id=user.id,
        topic=True
    )
    db.session.add(topic_discourseme)
    db.session.commit()
    log.debug('Created topic discourseme %s', topic_discourseme.id)

    # Add Analysis to DB
    analysis = Analysis(name=name,
                        corpus=corpus_name,
                        user_id=user.id,
                        topic_id=topic_discourseme.id,
                        max_window_size=max_window_size,
                        p_query=p_query,
                        s_break=s_break)
    db.session.add(analysis)
    db.session.commit()
    log.debug('Created analysis %s', analysis.id)

    # collocates: dict of dataframes with key == window_size
    collocates = dict()
    for window in range(1, max_window_size):
        collocates[window] = get_collocates(
            corpus_name=analysis.corpus,
            topic_items=items,
            s_context=s_break,
            window_size=window,
            context=analysis.max_window_size,
            p_query=p_query,
            s_query=None,
            ams=None,
            cut_off=cut_off,
            order=order
        )

    # Get Tokens for coordinate generation
    # TODO: I'm sure there's a one liner to do this
    tokens = []
    for df in collocates.values():
        tokens.extend(df.index)
    tokens = list(set(tokens))
    log.debug('Extracted  %d tokens for analysis %s' % (len(tokens), analysis.id))

    # no result?
    if len(tokens) == 0:
        log.debug('No collocates for query found for %s', items)
        db.session.delete(analysis)
        db.session.delete(topic_discourseme)
        db.session.commit()
        log.debug('Analysis deleted from database')
        return jsonify({'msg': 'Empty result'}), 404

    # Generate Coordinates
    log.debug('Generating semantic space for analysis %s', analysis.id)
    semantic_space = generate_semantic_space(
        tokens,
        current_app.config['CORPORA'][analysis.corpus]['embeddings']
    )
    coordinates = Coordinates(analysis_id=analysis.id)
    coordinates.data = semantic_space
    db.session.add(coordinates)
    db.session.commit()

    log.debug('Analysis created with ID %s', analysis.id)
    return jsonify({'msg': analysis.id}), 201


# READ
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/',
    methods=['GET']
)
@user_required
def get_analysis(username, analysis):
    """
    Get the details for an analysis.
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Analysis from DB
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Get and add topic discourseme details
    discourseme = Discourseme.query.filter_by(id=analysis.topic_id).first()
    analysis_dict = analysis.serialize
    analysis_dict['topic_discourseme'] = discourseme.serialize

    return jsonify(analysis_dict), 200


# READ
@analysis_blueprint.route(
    '/api/user/<username>/analysis/',
    methods=['GET']
)
@user_required
def get_all_analysis(username):
    """
    List all analyses for a user.
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    analyses = Analysis.query.filter_by(user_id=user.id).all()
    analyses_list = [analysis.serialize for analysis in analyses]

    return jsonify(analyses_list), 200


# UPDATE
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/',
    methods=['PUT']
)
@expects_json(UPDATE_SCHEMA)
@user_required
def update_analysis(username, analysis):
    """
    Update an analysis
    """

    # Check request
    name = request.json.get('name', None)
    # p_query = request.json.get('p_query', None)
    # s_break = request.json.get('s_break', None)
    # window_size = request.json.get('window_size', 0)

    if not name:
        log.debug('No name provided for analysis %s', analysis)
        return jsonify({'msg': 'Incorrect request data provided'}), 400

    # Get User
    user = User.query.filter_by(username=username).first()

    # Update analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    analysis.name = name

    db.session.commit()

    log.debug('Updated Analysis with ID %s', analysis)
    return jsonify({'msg': analysis.id}), 200


# DELETE
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/',
    methods=['DELETE']
)
@user_required
def delete_analysis(username, analysis):
    """
    Delete an analysis for a user.
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Remove Analysis from DB
    analysis = Analysis.query.filter_by(
        id=analysis, user_id=user.id
    ).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Change topic discourseme to regular discourseme
    discourseme = Discourseme.query.filter_by(
        id=analysis.topic_id,
        user_id=user.id
    ).first()
    discourseme.topic = False

    db.session.delete(analysis)
    db.session.commit()

    log.debug('Deleted Analysis with ID %s', analysis)
    return jsonify({'msg': 'Deleted'}), 200


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
    """
    Return a list of discoursemes for an analysis
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Analysis from DB
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Get Discoursemes list from DB
    analysis_discoursemes = [
        discourseme.serialize for discourseme in analysis.discourseme
    ]
    if not analysis_discoursemes:
        log.debug('No disoursemes associated')
        return jsonify([]), 200

    return jsonify(analysis_discoursemes), 200


# UPDATE
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/discourseme/<discourseme>/',
    methods=['PUT']
)
@user_required
def put_discourseme_into_analysis(username, analysis, discourseme):
    """
    Associate a discourseme with an analysis.

    parameters:
      - name: username
        description: username, links to user
      - name: analysis
        description: analysis_id, links to topic discourseme + query parameters
      - name: discourseme
        description: discourseme id to associate
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Analysis from DB
    analysis = Analysis.query.filter_by(
        id=analysis, user_id=user.id
    ).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Get Discourseme from DB
    discourseme = Discourseme.query.filter_by(
        id=discourseme, user_id=user.id
    ).first()
    if not discourseme:
        log.debug('No such discourseme %s', discourseme)
        return jsonify({'msg': 'No such discourseme'}), 404

    # Check if already linked or discourseme is topic discourseme of the analysis
    analysis_discourseme = AnalysisDiscoursemes.query.filter_by(
        analysis_id=analysis.id, discourseme_id=discourseme.id
    ).first()
    is_own_topic_discourseme = discourseme.id == analysis.topic_id
    if is_own_topic_discourseme:
        log.debug('Discourseme %s is already topic discourseme if the analysis',
                  discourseme)
        return jsonify({'msg': 'Is already topic'}), 409
    if analysis_discourseme:
        log.debug('Discourseme %s is already linked',
                  discourseme)
        return jsonify({'msg': 'Already linked'}), 200

    # Get topic discourseme
    topic_discourseme = Discourseme.query.filter_by(
        id=analysis.topic_id
    ).first()

    # Add link to DB
    analysis_discourseme = AnalysisDiscoursemes(
        analysis_id=analysis.id, discourseme_id=discourseme.id
    )
    db.session.add(analysis_discourseme)

    # extract all collocates
    # dict of dataframes with key === window_size
    collocates = dict()
    for window in range(1, analysis.max_window_size):
        collocates[window] = get_collocates(
            corpus_name=analysis.corpus,
            topic_items=topic_discourseme.items,
            s_context=analysis.s_break,
            window_size=window,
            context=analysis.max_window_size,
            p_query=analysis.p_query,
            additional_discoursemes={str(discourseme.id): discourseme.items},
            s_query=None,
            ams=None,
            cut_off=200,
            order='log_likelihood'
        )

    tokens = []
    for df in collocates.values():
        tokens.extend(df.index)
    tokens = list(set(tokens))

    log.debug('Generating Coordinates for missing collocates')
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    semantic_space = coordinates.data

    new_coordinates = generate_discourseme_coordinates(
        discourseme.items,
        semantic_space,
        current_app.config['CORPORA'][analysis.corpus]['embeddings']
    )
    if not new_coordinates.empty:
        log.debug('Appending new coordinates to semantic space')
        semantic_space.append(new_coordinates, sort=True)
        coordinates.data = semantic_space

    db.session.commit()

    log.debug('Added discourseme %s to analysis %s', discourseme, analysis)
    return jsonify({'msg': 'Updated'}), 200


# DELETE
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/discourseme/<discourseme>/',
    methods=['DELETE']
)
@user_required
def delete_discourseme_from_analysis(username, analysis, discourseme):
    """
    Remove a discourseme into from analysis
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Analysis from DB
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Get Discourseme from DB
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        log.debug('No such discourseme %s', discourseme)
        return jsonify({'msg': 'No such discourseme'}), 404

    # Check Link
    analysis_discourseme = AnalysisDiscoursemes.query.filter_by(
        analysis_id=analysis.id,
        discourseme_id=discourseme.id
    ).first()
    if not analysis_discourseme:
        log.warn('Discourseme %s not linked to analysis %s', discourseme, analysis)
        return jsonify({'msg': 'Not found'}), 404

    db.session.delete(analysis_discourseme)
    db.session.commit()

    log.debug('Removed discourseme %s to analysis %s', discourseme, analysis)
    return jsonify({'msg': 'Deleted'}), 200


##############
# COLLOCATES #
##############

@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/collocate/',
    methods=['GET']
)
@user_required
def get_collocate_for_analysis(username, analysis):
    """
    Get a collocate table for analysis.

    parameters:
      - name: username
        description: username, links to user
      - name: analysis
        description: analysis_id, links to topic discourseme + query parameters
      - name: window_size
        type: int
        description: window size for context (will be converted to int if necessary)
      - name: discourseme
        type: list
        required: False
        description: discourseme id(s) to include in discursive position
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
        description: concordance
      400:
        description: Error: Wrong request parameters
      404:
        description: Error: Empty result
    """
    # TODO: rename collocate ./. items

    # check request
    # ... user
    user = User.query.filter_by(username=username).first()
    # ... analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'Empty result'}), 404
    # ... window size
    window_size = request.args.get('window_size', 3)
    try:
        window_size = int(window_size)
    except TypeError:
        log.debug('Wrong type of window size')
        return jsonify({'msg': 'No data available'}), 400
    # ... optional discourseme ID list
    discourseme_ids = request.args.getlist('discourseme', None)
    # ... optional additional items
    items = request.args.getlist('collocate', None)
    # ... how many?
    cut_off = request.args.get('cut_off', 200)
    # ... how to sort them?
    order = request.args.get('order', 'log_likelihood')

    # pre-process request
    # ... get associated topic discourseme
    topic_discourseme = Discourseme.query.filter_by(id=analysis.topic_id).first()
    # ... floating discoursemes
    additional_discoursemes = dict()
    if items:
        # create discourseme for additional items on the fly
        additional_discoursemes['temp'] = items
    if discourseme_ids:
        # get all discoursemes from database and append
        discoursemes = Discourseme.query.filter(
            Discourseme.id.in_(discourseme_ids), Discourseme.user_id == user.id
        ).all()
        for d in discoursemes:
            additional_discoursemes[str(d.id)] = d.items

    # use cwb-ccc to extract data
    collocates = get_collocates(
        corpus_name=analysis.corpus,
        topic_items=topic_discourseme.items,
        s_context=analysis.s_break,
        window_size=window_size,
        context=analysis.max_window_size,
        additional_discoursemes=additional_discoursemes,
        p_query=analysis.p_query,
        s_query=None,
        ams=None,
        cut_off=cut_off,
        order=order
    )

    if collocates.empty:
        log.debug('No collocates available for window size %s', window_size)
        return jsonify({'msg': 'Empty result'}), 404

    # post-process result
    df = collocates.to_dict()

    return jsonify(df), 200


#####################
# CONCORDANCE LINES #
#####################
@analysis_blueprint.route(
    '/api/user/<username>/analysis/<analysis>/concordance/',
    methods=['GET']
)
@user_required
def get_concordance_for_analysis(username, analysis):
    """
    Get concordance lines for analysis.

    parameters:
      - name: username
        description: username, links to user
      - name: analysis
        description: analysis_id, links to topic discourseme + query parameters
      - name: window_size
        type: int
        description: window size for context (will be converted to int if necessary)
      - name: discourseme
        type: list
        required: False
        description: discourseme id(s) to include in discursive position
      - name: item
        type: list
        required: False
        description: lose item(s) for additional discourseme to include
      - name: cut_off
        type: int
        description: how many lines? [100]
      - name: order
        type: str
        description: how to sort them? (column in result table) [random]
      - name: s_meta
        type: str
        description: what s-att-annotation to retrieve [analysis.s_break]
    responses:
      200:
        description: concordance
      400:
        description: Error: Wrong request parameters
      404:
        description: Error: Empty result
    """
    # TODO: rename item ./. items

    # check request
    # ... user
    user = User.query.filter_by(username=username).first()
    # ... analysis
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'Empty result'}), 404
    # ... window size
    window_size = request.args.get('window_size', 3)
    try:
        window_size = int(window_size)
    except TypeError:
        log.debug('Wrong type of window size')
        return jsonify({'msg': 'Wrong request parameters'}), 400
    # ... optional discourseme ID list
    discourseme_ids = request.args.getlist('discourseme', None)
    # ... optional additional items
    items = request.args.getlist('item', None)
    # ... how many?
    cut_off = request.args.get('cut_off', 100)
    # ... how to sort them?
    order = request.args.get('order', 'random')
    # ... where's the meta data?
    s_show = [request.args.get('s_meta', analysis.s_break)]

    # pre-process request
    # ... get associated topic discourseme
    topic_discourseme = Discourseme.query.filter_by(id=analysis.topic_id).first()
    # ... floating discoursemes
    additional_discoursemes = dict()
    if items:
        # create discourseme for additional items on the fly
        additional_discoursemes['temp'] = items
    if discourseme_ids:
        # get all discoursemes from database and append
        discoursemes = Discourseme.query.filter(
            Discourseme.id.in_(discourseme_ids), Discourseme.user_id == user.id
        ).all()
        for d in discoursemes:
            additional_discoursemes[str(d.id)] = d.items

    # use cwb-ccc to extract data
    concordance = get_concordance(
        corpus_name=analysis.corpus,
        topic_items=topic_discourseme.items,
        topic_name=topic_discourseme.name,
        s_context=analysis.s_break,
        window_size=window_size,
        context=analysis.max_window_size,
        additional_discoursemes=additional_discoursemes,
        p_query=analysis.p_query,
        p_show=list(set(['word', analysis.p_query])),
        s_show=s_show,
        s_query=None,
        order=order,
        cut_off=cut_off,
        form='dataframes'
    )

    if concordance.empty:
        log.debug('No concordance available for analysis %s', analysis)
        return jsonify({'msg': 'Empty result'}), 404

    # post-process result
    df = concordance.reset_index()
    df = df.set_index('match')
    df = df['df'].apply(lambda x: x.to_dict()).to_dict()

    return jsonify(df), 200
