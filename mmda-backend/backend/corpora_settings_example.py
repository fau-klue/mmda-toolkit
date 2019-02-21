"""
Corpus specific settings
Contains the available corpora on the system

name: Human-readable name
name_api: Name used in Flask-API
wectors: Path to pymagnitude word vectors
language: Language of corpus
genre: Genre of the corpus
s_att: s-attribute for concordance and collocation delimitation
p_att: p-attribute for collocation extraction
association_measures: Available ssociation measures in the Engine
engine: Engine the corpus uses
"""

CORPORA = {
    'LTWBY2018': {
        'name': 'Tweets zur Landtagswahl in Bayern 2018',
        'name_api': 'LTWBY2018',
        'wectors': '/opt/wectors/magnitude/deTwitterWord2Vec.magnitude',
        'language': 'de',
        'genre': 'Social Media Discourse',
        's_att': 'tweet',
        'p_att': 'tt_lemma',
        'association_measures': ['am.simple.ll',
                                 'am.log.likelihood',
                                 'am.Dice',
                                 'am.MI'],
        'engine': 'CWBEngine'
    },
    'SZ_RANDOM': {
        'name': 'Süddeutsche Zeitung (mit RandomEngine)',
        'name_api': 'SZ_SMALL',
        'wectors': '/opt/wector/wiki-twitter-300d-1M-subword.magnitude',
        'language': 'de',
        'genre': 'Social Media Discourse',
        'sentence_boundary': 's',
        'association_measures': ['am.simple.ll', 'am.log.likelihood', 'am.Dice,am.MI'],
        'engine': 'RandomEngine'
    },
    'FAZ_DUMMY': {
        'name': 'FAZ Zeitung (mit DummyEngine)',
        'name_api': 'FAZ_SMALL',
        'wectors': '/opt/wector/wiki-news-300d-1M-subword.magnitude',
        'language': 'de',
        'genre': 'Newspaper',
        'sentence_boundary': 'tweet',
        'association_measures': ['am.simple.ll', 'am.log.likelihood', 'am.Dice,am.MI'],
        'engine': 'DummyEngine'
    }
}


ENGINES = {} # Gets populated when application starts
