"""
Corpus view
"""


from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from logging import getLogger

corpus_blueprint = Blueprint('corpus', __name__, template_folder='templates')
log = getLogger('mmda-logger')


# READ
@corpus_blueprint.route('/api/corpus/', methods=['GET'])
@jwt_required
def get_corpora():
    """
    Returns a list of available corpora as JSON array with their details.
    """

    # Get and transform for Frontend
    corpora = current_app.config['CORPORA']
    ret = [corpus for corpus in corpora.values()]

    return jsonify(ret), 200


# READ
@corpus_blueprint.route('/api/corpus/<corpus>/', methods=['GET'])
@jwt_required
def get_corpus(corpus):
    """
    Returns details for a given corpus as JSON object.
    :param str corpus: Name of corpus to get details for.
    """

    # Get Corpus
    corpora = current_app.config['CORPORA']
    if corpus not in corpora.keys():
        log.debug('No such corpus %s', corpus)
        return jsonify({'msg': 'No such corpus'}), 404

    corpus = corpora[corpus]

    return jsonify(corpus), 200


# READ
@corpus_blueprint.route('/api/corpus/<corpus>/concordances/', methods=['GET'])
@jwt_required
def get_concordances(corpus):
    """
    Returns concordances for a list of items (tokens)
    """

    # Check Request
    window_size = request.args.get('window_size', 8)
    items = request.args.getlist('item', None)
    collocates = request.args.getlist('collocate', None)

    if not items:
        log.debug('No items provided')
        return jsonify({'msg': 'No items provided'}), 400

    # Get Corpus
    corpora = current_app.config['CORPORA']
    if corpus not in corpora.keys():
        log.debug('No such corpus %s', corpus)
        return jsonify({'msg': 'No such corpus'}), 404

    corpus = corpora[corpus]
    # Get Engine
    engine = current_app.config['ENGINES'][corpus['name_api']]
    log.debug('Extracting concordances from %s', corpus)
    concordances = engine.extract_concordances(items=items, window_size=window_size, collocates=collocates)

    return jsonify(concordances), 200
