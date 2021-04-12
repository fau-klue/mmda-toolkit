"""
Corpus view
"""


from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required
from logging import getLogger
from backend.analysis.ccc import ccc_corpora, ccc_corpus


corpus_blueprint = Blueprint('corpus', __name__, template_folder='templates')
log = getLogger('mmda-logger')


# READ
@corpus_blueprint.route('/api/corpus/', methods=['GET'])
@jwt_required()
def get_corpora():
    """
    Returns a list of available corpora as JSON array with their details.
    """

    # Get and transform for Frontend
    corpora = current_app.config['CORPORA']
    cwb_corpora = ccc_corpora()
    ret = list()
    for corpus in corpora.values():
        if corpus['name_api'] in cwb_corpora.index:
            crps = ccc_corpus(corpus['name_api'])
            corpus['pQueries'] = crps['p-atts']
            corpus['sBreaks'] = crps['s-atts']
            ret.append(corpus)
    return jsonify(ret), 200


# READ
@corpus_blueprint.route('/api/corpus/<corpus>/', methods=['GET'])
@jwt_required()
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
