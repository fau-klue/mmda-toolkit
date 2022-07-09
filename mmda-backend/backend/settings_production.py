#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Corpus specific settings
Contains the available corpora on the system

name: Human-readable name
name_api: CWB handle of the corpus
embeddings: Path to pymagnitude word vectors
[language]: Language of corpus
[register]: Register of corpus
[description]:
"""


from os import getenv

# CWB-CCC PATHS
CCC_REGISTRY_PATH = getenv('CWB_REGISTRY_PATH', default='/usr/local/share/cwb/registry')
CCC_DATA_PATH = getenv('CCC_DATA_PATH', None)
CCC_CQP_BIN = getenv('CQP_BIN', default='cqp')
CCC_LIB_PATH = getenv('CCC_LIB_PATH', None)

# DATABASE URI
SQLALCHEMY_DATABASE_URI = getenv(
    'SQL_DATABASE_URI',
    'sqlite:////opt/database/mmda.sqlite'
)

CORPORA = {
    'BREXIT_V190615': {
        'name': 'BREXIT_V190615',
        'name_api': 'Brexit tweets',
        'embeddings': '/opt/embeddings/enTwitterWord2Vec.magnitude',
        'language': 'en',
        'register': 'cmc',
        'description': 'test'
    },
}
