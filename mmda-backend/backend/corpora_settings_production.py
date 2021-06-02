"""
Corpus specific settings
Contains the available corpora on the system

name: Human-readable name
name_api: CWB handle of the corpus
embeddings: Path to pymagnitude word vectors
language: Language of corpus
register: Register of the corpus
"""

CORPORA = {
    'INFODEMIC_TWITTER_USERS': {
        'name': 'Infodemic: Twitter Users',
        'name_api': 'INFODEMIC_TWITTER_USERS',
        'embeddings': '/opt/embeddings/deTwitterWord2Vec.magnitude',
        'language': 'de',
        'register': 'cmc'
    },
    'CORONA_DE_V1': {
        'name': 'Infodemic: Twitter (March-May 2020)',
        'name_api': 'CORONA_DE_V1',
        'embeddings': '/opt/embeddings/deTwitterWord2Vec.magnitude',
        'language': 'de'
    },
    'BREXIT_V20190522_DEDUP': {
        'name': 'Brexit Tweets (2016)',
        'name_api': 'BREXIT_V20190522_DEDUP',
        'embeddings': '/opt/embeddings/deTwitterWord2Vec.magnitude',
        'language': 'en'
    },
    'GERMAPARL1318': {
        'name': 'GermaParl (1996-2006)',
        'name_api': 'GERMAPARL1318',
        'embeddings': '/opt/embeddings/deTwitterWord2Vec.magnitude',
        'language': 'de',
        'description': "Deutscher Bundestag"
    },
    'SZ_2009_14': {
        'name': 'Süddeutsche Zeitung (2009-2014)',
        'name_api': 'SZ_2009_14',
        'embeddings': '/opt/embeddings/deTwitterWord2Vec.magnitude',
        'language': 'de'
    },
    'TWEETS_JAP_PHASE_OUT': {
        'name': 'Japanese tweets about phase-out',
        'name_api': 'TWEETS_JAP_PHASE_OUT',
        'embeddings': '/opt/embeddings/deTwitterWord2Vec.magnitude',
        'language': 'jap'
    },
    'YOMIURI': {
        'name': 'Yomiuri',
        'name_api': 'YOMIURI',
        'embeddings': '/opt/embeddings/deTwitterWord2Vec.magnitude',
        'language': 'jap'
    }
}
