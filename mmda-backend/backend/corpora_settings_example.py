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
    'SZ_SMALL': {
        'name': 'Süddeutsche Zeitung',
        'name_api': 'SZ_SMALL',
        'wectors': '/opt/wector/wiki-news-300d-1M-subword.magnitude',
        'language': 'de',
        'genre': 'Social Media Discourse',
        'sentence_boundary': 's',
        'association_measures': ['am.simple.ll', 'am.log.likelihood', 'am.Dice,am.MI'],
        'engine': 'DummyEngine'
    },
    'FAZ_SMALL': {
        'name': 'FAZ Zeitung',
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
