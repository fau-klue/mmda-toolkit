"""
Analysis view
"""


from flask import Blueprint, request, jsonify, current_app
from flask_expects_json import expects_json
from logging import getLogger

from backend import db
from backend import user_required
from backend.analysis.ccc import ConcordanceCollocationCalculator as CCC

from backend.analysis.validators import ANALYSIS_SCHEMA, UPDATE_SCHEMA
from backend.analysis.coordinates.tsne import generate_semantic_space, generate_discourseme_coordinates
from backend.models.user_models import User
from backend.models.analysis_models import Analysis, AnalysisDiscoursemes, Discourseme, Coordinates

analysis_blueprint = Blueprint('analysis', __name__, template_folder='templates')
log = getLogger('mmda-logger')


# CREATE
@analysis_blueprint.route('/api/user/<username>/analysis/', methods=['POST'])
@expects_json(ANALYSIS_SCHEMA)
@user_required
def create_analysis(username):
    """
    Add a new analysis for a user
    """

    # Check Request
    name = request.json.get('name', None)
    corpus = request.json.get('corpus', None)
    maximal_window_size = request.json.get('window_size', 3)
    p_query = request.json.get('p_query', None)
    s_break = request.json.get('s_break', None)
    association_measures = request.json.get('association_measures', [])
    items = request.json.get('items', [])

    # Check corpus
    if corpus not in current_app.config['CORPORA']:
        log.debug('No such corpus %s', corpus)
        return jsonify({'msg': 'Corpus not available'}), 400

    # Get User
    user = User.query.filter_by(username=username).first()

    # Add Discourseme to DB
    topic_discourseme = Discourseme(name=name, items=items, user_id=user.id, topic=True)
    db.session.add(topic_discourseme)
    db.session.commit()
    log.debug('Created topic discourseme %s', topic_discourseme.id)

    # Add Analysis to DB
    analysis = Analysis(name=name,
                        corpus=corpus,
                        user_id=user.id,
                        topic_id=topic_discourseme.id,
                        window_size=maximal_window_size,
                        p_query=p_query,
                        s_break=s_break,
                        association_measures=association_measures)

    db.session.add(analysis)
    db.session.commit()
    log.debug('Created analysis %s', analysis.id)

    # Load Collocates
    engine = current_app.config['ENGINES'][analysis.corpus]
    ccc = CCC(analysis, engine)

    collocates = ccc.extract_collocates(topic_discourseme)

    # Get Tokens for coordinate generation
    # collocates is a dict of dataframes with key == window_size
    # TODO: I'm sure there's a one liner to do this
    tokens = []
    for df in collocates.values():
        tokens.extend(df.index)
    tokens = list(set(tokens))
    log.debug('Extracted tokens for analysis %s: %s', analysis.id, tokens)

    if len(tokens) == 0:
        log.warn('No collocates for query found for %s', items)
        db.session.delete(analysis)
        db.session.delete(topic_discourseme)
        db.session.commit()
        log.debug('Analysis deleted from database')
        return jsonify({'msg': 'No collocates for query found.'}), 404

    # Generate Coordinates
    log.debug('Generating semantic space for analysis %s', analysis.id)
    wectors_path = current_app.config['CORPORA'][analysis.corpus]['wectors']
    semantic_space = generate_semantic_space(tokens, wectors_path)

    coordinates = Coordinates(analysis_id=analysis.id)
    coordinates.data = semantic_space

    db.session.add(coordinates)
    db.session.commit()

    log.debug('Analysis created with ID %s', analysis.id)
    return jsonify({'msg': analysis.id}), 201


# READ
@analysis_blueprint.route('/api/user/<username>/analysis/<analysis>/', methods=['GET'])
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
@analysis_blueprint.route('/api/user/<username>/analysis/', methods=['GET'])
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
@analysis_blueprint.route('/api/user/<username>/analysis/<analysis>/', methods=['PUT'])
@expects_json(UPDATE_SCHEMA)
@user_required
def update_analysis(username, analysis):
    """
    Update an analysis
    """

    # Check request
    name = request.json.get('name', None)
    p_uqery = request.json.get('p_query', None)
    s_break = request.json.get('s_break', None)
    window_size = request.json.get('window_size', 0)

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
@analysis_blueprint.route('/api/user/<username>/analysis/<analysis>/', methods=['DELETE'])
@user_required
def delete_analysis(username, analysis):
    """
    Delete an analysis for a user.
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Remove Analysis from DB
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Change topic discourseme to regular discourseme
    discourseme = Discourseme.query.filter_by(id=analysis.topic_id, user_id=user.id).first()
    discourseme.topic = False

    db.session.delete(analysis)
    db.session.commit()

    log.debug('Deleted Analysis with ID %s', analysis)
    return jsonify({'msg': 'Deleted'}), 200


# READ
@analysis_blueprint.route('/api/user/<username>/analysis/<analysis>/discourseme/', methods=['GET'])
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
    analysis_discoursemes = [discourseme.serialize for discourseme in analysis.discourseme]
    if not analysis_discoursemes:
        log.debug('No disoursemes associated')
        return jsonify([]), 200

    return jsonify(analysis_discoursemes), 200


# UPDATE
@analysis_blueprint.route('/api/user/<username>/analysis/<analysis>/discourseme/<discourseme>/', methods=['PUT'])
@user_required
def put_discourseme_into_analysis(username, analysis, discourseme):
    """
    Add a discourseme into an analysis
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

    # Check if already linked or discourseme is topic discourseme of the analysis
    analysis_discourseme = AnalysisDiscoursemes.query.filter_by(analysis_id=analysis.id, discourseme_id=discourseme.id).first()

    is_own_topic_discourseme = discourseme.id == analysis.topic_id
    if is_own_topic_discourseme:
        log.debug('Discourseme %s is already topic discourseme if the analysis', discourseme)
        return jsonify({'msg': 'Is already topic'}), 409

    if analysis_discourseme:
        log.debug('Discourseme %s is already linked', discourseme)
        return jsonify({'msg': 'Already linked'}), 200

    # Add Link to DB
    analysis_discourseme = AnalysisDiscoursemes(analysis_id=analysis.id, discourseme_id=discourseme.id)
    db.session.add(analysis_discourseme)

    # Load Collocates
    engine = current_app.config['ENGINES'][analysis.corpus]
    ccc = CCC(analysis, engine)

    # Get Topic Discourseme
    topic_discourseme = Discourseme.query.filter_by(id=analysis.topic_id).first()

    # TODO: Parameter? Cut Off?
    collocates = ccc.extract_collocates(topic_discourseme, [discourseme])

    # dict of dataframes with key === window_size
    tokens = []
    for df in collocates.values():
        tokens.extend(df.index)
    tokens = list(set(tokens))

    log.debug('Generating Coordinates for missing collocates')
    coordinates = Coordinates.query.filter_by(analysis_id=analysis.id).first()
    semantic_space = coordinates.data
    wectors_path = current_app.config['CORPORA'][analysis.corpus]['wectors']

    new_coordinates = generate_discourseme_coordinates(discourseme.items, semantic_space, wectors_path)
    if not new_coordinates.empty:
        log.debug('Appending new coordinates to semantic space')
        semantic_space.append(new_coordinates, sort=True)
        coordinates.data = semantic_space

    db.session.commit()

    log.debug('Added discourseme %s to analysis %s', discourseme, analysis)
    return jsonify({'msg': 'Updated'}), 200


# DELETE
@analysis_blueprint.route('/api/user/<username>/analysis/<analysis>/discourseme/<discourseme>/', methods=['DELETE'])
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
    analysis_discourseme = AnalysisDiscoursemes.query.filter_by(analysis_id=analysis.id, discourseme_id=discourseme.id).first()
    if not analysis_discourseme:
        log.warn('Discourseme %s not linked to analysis %s', discourseme, analysis)
        return jsonify({'msg': 'Not found'}), 404

    db.session.delete(analysis_discourseme)
    db.session.commit()

    log.debug('Removed discourseme %s to analysis %s', discourseme, analysis)
    return jsonify({'msg': 'Deleted'}), 200


# READ
@analysis_blueprint.route('/api/user/<username>/analysis/<analysis>/collocate/', methods=['GET'])
@user_required
def get_collocate_for_analysis(username, analysis):
    """
    Get a collocate table for an analysis
    """

    # Check Request
    window_size = request.args.get('window_size', 3)
    # Second order collocates
    collocates = request.args.getlist('collocate', None)

    if not window_size and not collocates:
        log.debug('No window size and collocates provided')
        return jsonify({'msg': 'No request data provided'}), 400

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Analysis from DB
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Get Topic Discourseme
    topic_discourseme = Discourseme.query.filter_by(id=analysis.topic_id).first()

    # Get topic and items
    engine = current_app.config['ENGINES'][analysis.corpus]
    ccc = CCC(analysis, engine)

    # TODO: Parameter? Cut Off?
    collocates = ccc.extract_collocates(topic_discourseme)

    df = collocates[window_size].to_dict()

    if not df:
        log.debug('No collocates available for analysis %s', analysis)
        return jsonify({'msg': 'No collocates available'}), 404

    return jsonify(df), 200


# READ
@analysis_blueprint.route('/api/user/<username>/analysis/<analysis>/concordance/', methods=['GET'])
@user_required
def get_concordance_for_analysis(username, analysis):
    """
    Get concordance for an analysis
    """

    # Check Request
    window_size = request.args.get('window_size', 3)

    try:
        window_size = int(window_size)
    except TypeError:
        log.debug('No window size')
        return jsonify({'msg': 'No request data provided'}), 400
    except ValueError:
        log.debug('Window size must be integer')
        return jsonify({'msg': 'Window size must be integer'}), 400

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Analysis from DB
    analysis = Analysis.query.filter_by(id=analysis, user_id=user.id).first()
    if not analysis:
        log.debug('No such analysis %s', analysis)
        return jsonify({'msg': 'No such analysis'}), 404

    # Get Topic Discourseme
    topic_discourseme = Discourseme.query.filter_by(id=analysis.topic_id).first()

    # Get topic and items
    engine = current_app.config['ENGINES'][analysis.corpus]
    ccc = CCC(analysis, engine)

    # TODO: Parameter? Cut Off?
    concordance = ccc.extract_concordance(topic_discourseme)

    if not window_size in concordance.keys():
        log.debug('No collocates available for window size %s', window_size)
        return jsonify({'msg': 'No collocates available for window size'}), 404

    df = concordance[window_size].to_dict()

    if not df:
        log.debug('No collocates available for analysis %s', analysis)
        return jsonify({'msg': 'No collocates available'}), 404

    return jsonify(df), 200
