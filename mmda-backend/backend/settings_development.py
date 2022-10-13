#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Development settings
"""

from os import getenv

# CWB-CCC PATHS
CCC_REGISTRY_PATH = getenv('CWB_REGISTRY_PATH', default='/usr/local/share/cwb/registry')
CCC_DATA_PATH = getenv(
    'CCC_DATA_PATH',
    default='/home/ausgerechnet/implementation/mmda-toolkit/mmda-backend/instance/ccc-data-development/'
)
CCC_CQP_BIN = getenv('CQP_BIN', default='cqp')
CCC_LIB_PATH = getenv('CCC_LIB_PATH', None)

# DATABASE URI
SQLALCHEMY_DATABASE_URI = getenv(
    'SQL_DATABASE_URI',
    'sqlite:////home/ausgerechnet/implementation/mmda-toolkit/mmda-backend/instance/mmda-development.sqlite'
)

# CORPORA
CORPORA = {
    'COV_PRESSE_DE': {
        'name': 'Infodemic: Presseartikel (DE)',
        'name_api': 'COV_PRESSE_DE',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deWikiWord2Vec.magnitude',
        'language': 'de'
    },
    'COV_PRESSE_FR': {
        'name': 'Infodemic: Presseartikel (FR)',
        'name_api': 'COV_PRESSE_FR',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/frWikiWord2Vec.magnitude',
        'language': 'fr'
    },
    'GEREDE_V2_DEV0': {
        'name': 'GeRedE (2010 - 2021)',
        'name_api': 'GEREDE_V2_DEV0',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deTwitterWord2Vec.magnitude',
        'language': 'de'
    },
    'CORONA_DE_V1': {
        'name': 'Infodemic: Twitter (March 2020 - May 2020)',
        'name_api': 'CORONA_DE_V1',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deTwitterWord2Vec.magnitude',
        'language': 'de'
    },
    'CORONA_DE_V2': {
        'name': 'Infodemic: Twitter (June 2020 - April 2021)',
        'name_api': 'CORONA_DE_V2',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deTwitterWord2Vec.magnitude',
        'language': 'de'
    },
    'INFODEMIC_TWITTER_USERS_V4': {
        'name': 'Infodemic: Twitter Users (2020 - 2021)',
        'name_api': 'INFODEMIC_TWITTER_USERS_V4',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deTwitterWord2Vec.magnitude',
        'language': 'de'
    },
    'INFODEMIC_TELEGRAM': {
        'name': 'Infodemic: Telegram (June 2020 - April 2021)',
        'name_api': 'INFODEMIC_TELEGRAM',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deTwitterWord2Vec.magnitude',
        'language': 'de'
    },
    'SPRITZER_DE_2020_2021': {
        'name': 'German Reference Tweets (2020 - 2021)',
        'name_api': 'SPRITZER_DE_2020_2021',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deTwitterWord2Vec.magnitude',
        'language': 'de'
    },
    # 'BREXIT_V20190522_DEDUP': {
    #     'name': 'Brexit Tweets (2016)',
    #     'name_api': 'BREXIT_V20190522_DEDUP',
    #     'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/enTwitterWord2Vec.magnitude',
    #     'language': 'en'
    # },
    'GERMAPARL1318': {
        'name': 'GermaParl (1996-2006)',
        'name_api': 'GERMAPARL1318',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deWikiWord2Vec.magnitude',
        'language': 'de',
        'description': "Deutscher Bundestag"
    },
    'SZ_2011_14': {
        'name': 'Süddeutsche Zeitung (2011 - 2014)',
        'name_api': 'SZ_2011_14',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deWikiWord2Vec.magnitude',
        'language': 'de'
    },
    'SZ_2019_2020': {
        'name': 'Süddeutsche Zeitung (2019 - 2020)',
        'name_api': 'SZ_2019_2020',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deWikiWord2Vec.magnitude',
        'language': 'de'
    },
    'FAZ_2011_14': {
        'name': 'Frankfurter Allgemeine Zeitung (2011 - 2014)',
        'name_api': 'FAZ_2011_14',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deWikiWord2Vec.magnitude',
        'language': 'de'
    },
    # 'TWEETS_JAP_PHASE_OUT': {
    #     'name': 'Japanese tweets about phase-out',
    #     'name_api': 'TWEETS_JAP_PHASE_OUT',
    #     'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/jaTwitterWord2Vec.magnitude',
    #     'language': 'jap'
    # },
    # 'YOMIURI': {
    #     'name': 'Yomiuri',
    #     'name_api': 'YOMIURI',
    #     'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/jaWikiWord2Vec.magnitude',
    #     'language': 'jap'
    # }
}
