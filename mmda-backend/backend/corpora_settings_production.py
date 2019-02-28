"""
Corpus specific settings
Contains the available corpora on the system

name: Human-readable name
wectors: Path to pymagnitude word vectors
language: Language of corpus
genre: Genre of the corpus
engine: Engine the corpus uses
association_measures: Available ssociation measures in the Engine
"""

CORPORA = {
    'LTWBY2018': {
        'name': 'Tweets zur Landtagswahl in Bayern 2018',
        'name_api': 'LTWBY2018',
        'wectors': '/opt/wectors/deTwitterWord2Vec.magnitude',
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
    'LTWBY2018': {
        'name': 'Austerity 0925',
        'name_api': 'AUSTERITY_0925',
        'wectors': '/opt/wectors/enWikiWord2Vec.magnitude',
        'language': 'en',
        'genre': 'Newspaper',
        's_att': 's',
        'p_att': 'tt_lemma',
        'association_measures': ['am.simple.ll',
                                 'am.log.likelihood',
                                 'am.Dice',
                                 'am.MI'],
        'engine': 'CWBEngine'
    },
    'LTWBY2018': {
        'name': 'Nachrichten zur Landtagswahl in Bayern 2018',
        'name_api': 'LTWBY2018',
        'wectors': '/opt/wectors/deWikiWord2Vec.magnitude',
        'language': 'de',
        'genre': 'Newspaper',
        's_att': 's',
        'p_att': 'tt_lemma',
        'association_measures': ['am.simple.ll',
                                 'am.log.likelihood',
                                 'am.Dice',
                                 'am.MI'],
        'engine': 'CWBEngine'
    },
}


ENGINES = {} # Gets populated when application starts
