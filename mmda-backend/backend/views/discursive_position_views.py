"""
Discursive Position views
"""


from flask import Blueprint, request, jsonify, current_app
from flask_expects_json import expects_json
from logging import getLogger

from backend import db
from backend import user_required
from backend.analysis.validators import (
    DISCURSIVE_POSITION_SCHEMA,
    DISCURSIVE_POSITION_UPDATE_SCHEMA
)
from backend.models.user_models import User
from backend.models.analysis_models import Analysis, Discourseme, DiscursivePositionDiscoursemes, DiscursivePosition
from backend.analysis.ccc import get_concordance

discursive_blueprint = Blueprint('discursive_position', __name__, template_folder='templates')
log = getLogger('mmda-logger')


# CREATE
@discursive_blueprint.route('/api/user/<username>/discursiveposition/', methods=['POST'])
@expects_json(DISCURSIVE_POSITION_SCHEMA)
@user_required
def create_discursive_position(username):
    """
    Add a new discursive position for a user.
    """

    # Check Request. Discoursemes should be List of IDs
    name = request.json.get('name', None)
    discoursemes = request.json.get('discoursemes', [])

    # Get User
    user = User.query.filter_by(username=username).first()

    # Create Position
    discursive = DiscursivePosition(name=name, user_id=user.id)
    db.session.add(discursive)
    db.session.commit()
    log.debug('Created Discursive Position %s', discursive.id)

    for discourseme_id in discoursemes:
        # Check if disourseme exists
        discourseme = Discourseme.query.filter_by(id=discourseme_id, user_id=user.id).first()
        if not discourseme:
            continue

        # Check if exists alread
        position_discourseme = DiscursivePositionDiscoursemes.query.filter_by(discursive_position_id=discursive.id, discourseme_id=discourseme.id).first()
        if position_discourseme:
            continue

        # Add discourseme link
        position_discourseme = DiscursivePositionDiscoursemes(discursive_position_id=discursive.id, discourseme_id=discourseme.id)
        db.session.add(position_discourseme)
        log.debug('Added Discourseme %s to Discursive Position %s', discourseme.id, discursive.id)

    db.session.commit()

    return jsonify({'msg': discursive.id}), 201


# READ
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/', methods=['GET'])
@user_required
def get_discursive_position(username, discursive_position):
    """
    Get details for a discursive position.
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        log.debug('No such Discursive Position %s', discursive_position)
        return jsonify({'msg': 'No such discursive position'}), 404

    # TODO: Add Discoursemes here as well?
    return jsonify(discursive.serialize), 200


# READ
@discursive_blueprint.route('/api/user/<username>/discursiveposition/', methods=['GET'])
@user_required
def get_discursive_positions(username):
    """
    List all discursive positions for a user.
    """

    # Get User
    user = User.query.filter_by(username=username).first()
    discursives = DiscursivePosition.query.filter_by(user_id=user.id).all()
    discursives_list = [discursive.serialize for discursive in discursives]

    return jsonify(discursives_list), 200


# UPDATE
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/', methods=['PUT'])
@expects_json(DISCURSIVE_POSITION_UPDATE_SCHEMA)
@user_required
def update_discursive_position(username, discursive_position):
    """
    Update discursive position details
    """

    # Check request
    name = request.json.get('name', None)

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Position from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        log.debug('No such Discursive Position %s', discursive_position)
        return jsonify({'msg': 'No such discursive position'}), 404

    discursive.name = name
    db.session.commit()
    log.debug('Updated Discursive Position %s', discursive_position)

    return jsonify({'msg': discursive.id}), 200


# DELETE
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/', methods=['DELETE'])
@user_required
def delete_discursive_position(username, discursive_position):
    """
    Delete a discursive position.
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Remove Position from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        log.debug('No such Discursive Position %s', discursive_position)
        return jsonify({'msg': 'No such discursive position'}), 404

    db.session.delete(discursive)
    db.session.commit()
    log.debug('Deleted Discursive Position %s', discursive_position)

    return jsonify({'msg': 'Deleted'}), 200


# READ
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/discourseme/', methods=['GET'])
@user_required
def get_discoursemes_for_discursive_position(username, discursive_position):
    """
    Return list of discoursemes for a discursive position
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Position from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        log.debug('No such Discursive Position %s', discursive_position)
        return jsonify({'msg': 'No such discursive position'}), 404

    # Get Discoursemes list from DB
    position_discoursemes = [discourseme.serialize for discourseme in discursive.discourseme]
    if not position_discoursemes:
        log.debug('Discursive Position %s has no Discoursemes associated', discursive.id)
        return jsonify([]), 200

    return jsonify(position_discoursemes), 200


# UPDATE
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/discourseme/<discourseme>/', methods=['PUT'])
@user_required
def put_discourseme_into_discursive_position(username, discursive_position, discourseme):
    """
    Put a discourseme into a discursive position
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Position from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        log.debug('No such Discursive Position %s', discursive_position)
        return jsonify({'msg': 'No such discursive position'}), 404

    # Get Discourseme from DB
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        log.debug('No such Discourseme %s', discourseme)
        return jsonify({'msg': 'No such discourseme'}), 404

    # Check if exists
    position_discourseme = DiscursivePositionDiscoursemes.query.filter_by(discursive_position_id=discursive.id, discourseme_id=discourseme.id).first()

    if position_discourseme:
        log.debug('Discourseme %s already linked to Discursive Position %s', discourseme, discursive_position)
        return jsonify({'msg': 'Already linked'}), 200

    # Add Link to DB
    position_discourseme = DiscursivePositionDiscoursemes(discursive_position_id=discursive.id, discourseme_id=discourseme.id)
    db.session.add(position_discourseme)
    db.session.commit()
    log.debug('Linked Discourseme %s to Discursive Position %s', discourseme, discursive_position)

    return jsonify({'msg': 'Updated'}), 200


# DELETE
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/discourseme/<discourseme>/', methods=['DELETE'])
@user_required
def delete_discourseme_from_discursive_position(username, discursive_position, discourseme):
    """
    Remove a discourseme from a discursive position
    """

    # Get User
    user = User.query.filter_by(username=username).first()

    # Get Position from DB
    discursive = DiscursivePosition.query.filter_by(id=discursive_position, user_id=user.id).first()
    if not discursive:
        log.debug('No such Discursive Position %s', discursive_position)
        return jsonify({'msg': 'No such discursive position'}), 404

    # Get Discourseme from DB
    discourseme = Discourseme.query.filter_by(id=discourseme, user_id=user.id).first()
    if not discourseme:
        log.debug('No such Discourseme %s', discourseme)
        return jsonify({'msg': 'No such discourseme'}), 404

    position_discourseme = DiscursivePositionDiscoursemes.query.filter_by(discursive_position_id=discursive.id, discourseme_id=discourseme.id).first()

    if not position_discourseme:
        log.debug('Discourseme %s is not linked to Discursive Position %s', discourseme, discursive_position)
        return jsonify({'msg': 'Not found'}), 404

    db.session.delete(position_discourseme)
    db.session.commit()
    log.debug('Unlinked Discourseme %s to Discursive Position %s', discourseme, discursive_position)

    return jsonify({'msg': 'Deleted'}), 200


# READ
@discursive_blueprint.route('/api/user/<username>/discursiveposition/<discursive_position>/concordance/', methods=['GET'])
@user_required
def get_discursive_position_concordances(username, discursive_position):
    """
    Get concordances for a discursive position.
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
    window_size = request.args.get('window_size', 3)
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
    # ... and the whole discoursem constellation
    discursive = DiscursivePosition.query.filter_by(
        id=discursive_position, user_id=user.id
    ).first()
    if not discursive:
        return jsonify({'msg': 'No such discursive position'}), 404
    # ... floating discoursemes
    additional_discoursemes = dict()
    if items:
        # create discourseme for additional items on the fly
        additional_discoursemes['temp'] = items
    if not discursive.discourseme:
        log.debug('Discursive Position %s has no Discoursemes associated', discursive.id)
    else:
        discourseme_ids = [d.id for d in discursive.discourseme]
        # get all discoursemes from database and append
        discoursemes = Discourseme.query.filter(
            Discourseme.id.in_(discourseme_ids), Discourseme.user_id == user.id
        ).all()
        for d in discoursemes:
            additional_discoursemes[str(d.id)] = d.items

    ret = {}
    for corpus in corpora:

        # use cwb-ccc to extract data
        concordance = get_concordance(
            corpus_name=corpus,
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
            log.debug('No concordances available for corpus %s', corpus)
            continue

        log.debug(
            'Extracted concordances for corpus %s with analysis %s', corpus, analysis
        )

        # post-process result
        df = concordance.reset_index()
        df = df.set_index('match')
        df = df['df'].apply(lambda x: x.to_dict()).to_dict()

        ret[corpus] = df

    return jsonify(ret), 200
