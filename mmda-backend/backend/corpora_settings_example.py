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
        'name': 'Example tweets in English',
        'name_api': 'MMDA_EN_TWEETS',
        'wectors': '/opt/wectors/magnitude/enTwitterWord2Vec.magnitude',
        'language': 'en',
        'genre': 'Social Media Discourse',
        's_att': ['corpus', 'text', 'tweet'],
        'p_att': ['word', 'pos', 'lemma'],
        'association_measures': ['simple.ll',
                                 'log.likelihood',
                                 'Dice',
                                 'MI'],
        'engine': 'CWBEngine',
        'registry_path': '/opt/cwb/registry'
    },
}


ENGINES = {}                  # Gets populated when application starts
