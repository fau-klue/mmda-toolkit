#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Production settings
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

# CORPORA
CORPORA = {
    'GERMAPARL1386': {
        'name': 'GERMAPARL1386',
        'name_api': 'GERMAPARL1386',
        'embeddings': '/opt/embeddings/deWikiWord2Vec.magnitude',
        'language': 'de',
        'register': 'standard',
        'description': 'Bundestag'
    },
}
