"""
Corpus view
"""


from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required
from logging import getLogger
from backend.analysis.ccc import ccc_corpus


corpus_blueprint = Blueprint('corpus', __name__, template_folder='templates')
log = getLogger('mmda-logger')


# READ
@corpus_blueprint.route('/api/corpus/', methods=['GET'])
@jwt_required()
def get_corpora():
    """
    Returns a list of available corpora as JSON array with their details.
    """

    # corpora defined by corpus_settings.py:
    corpora = list()
    for corpus in current_app.config['CORPORA'].values():

        # get corpus from CWB, see below for a commented version
        try:
            crps = ccc_corpus(corpus_name=corpus['name_api'],
                              cqp_bin=current_app.config['CCC_CQP_BIN'],
                              registry_path=current_app.config['CCC_REGISTRY_PATH'],
                              data_path=current_app.config['CCC_DATA_PATH'])
        except KeyError:
            return {'msg': 'corpus not available via CWB '}, 404
        corpus['pQueries'] = crps['p-atts']
        corpus['sBreaks'] = crps['s-atts']
        corpora.append(corpus)

    return jsonify(corpora), 200


# READ
@corpus_blueprint.route('/api/corpus/<corpus>/', methods=['GET'])
@jwt_required()
def get_corpus(corpus):
    """
    Returns details for a given corpus as JSON object.
    :param str corpus: API/CWB handle of the corpus
    """

    # get corpus settings from corpus_settings.py:
    corpora = current_app.config['CORPORA']
    if corpus not in corpora.keys():
        log.debug('corpus not in settings.py')
        return {'msg': 'corpus not in settings.py'}, 404
    corpus = corpora[corpus]

    # get corpus from CWB
    try:
        crps = ccc_corpus(corpus_name=corpus['name_api'],
                          cqp_bin=current_app.config['CCC_CQP_BIN'],
                          registry_path=current_app.config['CCC_REGISTRY_PATH'],
                          data_path=current_app.config['CCC_DATA_PATH'])
    except KeyError:
        return {'msg': 'corpus not available via CWB '}, 404

    # attribute lists will be displayed in frontend
    # they are sorted by the backend to provide suitable default values
    corpus['pQueries'] = crps['p-atts']
    corpus['sBreaks'] = crps['s-atts']

    return jsonify(corpus), 200
