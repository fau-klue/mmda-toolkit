# Corpus view


from flask import Blueprint, redirect, render_template, current_app, jsonify
from flask import request, url_for
from flask_jwt_extended import jwt_required

from backend import db
from backend import admin_required

corpus_blueprint = Blueprint('corpus', __name__, template_folder='templates')


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
    items = request.args.getlist('item')

    if not items:
        return jsonify({'msg': 'No items provided'}), 400

    # Get Corpus
    corpora = current_app.config['CORPORA']
    if corpus not in corpora.keys():
        return jsonify({'msg': 'No such corpus'}), 404

    corpus = corpora[corpus]
    # Get Engine
    engine = current_app.config['ENGINES'][corpus['name_api']]
    concordances = engine.extract_concordances(items, window_size)

    # TODO: Test if format is OK
    return jsonify(concordances), 200
