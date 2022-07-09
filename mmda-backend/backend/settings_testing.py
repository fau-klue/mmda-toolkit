"""
Test settings
"""

from os import getenv

# CWB-CCC PATHS
CCC_REGISTRY_PATH = getenv(
    'CWB_REGISTRY_PATH',
    default='/home/ausgerechnet/implementation/cwb-ccc/tests/corpora/registry/'
)
CCC_DATA_PATH = getenv(
    'CCC_DATA_PATH',
    default='/home/ausgerechnet/implementation/mmda-refactor/mmda-backend/instance/ccc-data-testing/'
)
CCC_CQP_BIN = getenv('CQP_BIN', default='cqp')
CCC_LIB_PATH = getenv('CCC_LIB_PATH', None)

# DATABASE URI
SQLALCHEMY_DATABASE_URI = getenv(
    'SQL_DATABASE_URI',
    "sqlite:///:memory:"
)

CORPORA = {
    'GERMAPARL1386': {
        'name': 'GermaParl',
        'name_api': 'GERMAPARL1386',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deWikiWord2Vec.magnitude',
        'language': 'de',
    }
}
