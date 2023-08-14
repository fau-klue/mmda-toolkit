"""MMDA Backend Settings

"""
from os import getenv


################################
# SET VIA ENVIRONMENT VARIABLES
################################

# ENVIRONMENT
APP_ENV = str(getenv('ENVIRONMENT', default='development'))

# SECRET KEY
SECRET_KEY = str(getenv('SECRET_KEY', default='Please Change me in production. Stay Save!'))

# DATABASE
SQLALCHEMY_DATABASE_URI = str(getenv('SQL_DATABASE_URI', default='sqlite:///mmda.sqlite'))

# CORPORA
CORPORA_SETTINGS = str(getenv('CORPORA_SETTINGS', default='../tests/corpora/corpora.py'))

# CWB-CCC
CCC_REGISTRY_DIR = str(getenv('CORPUS_REGISTRY', default='tests/corpora/registry/'))
CCC_CQP_BIN = str(getenv('CQP_BIN', default='cqp'))
CCC_LIB_DIR = getenv('CCC_LIB_DIR', None)

# CACHE
CCC_DATA_DIR = str(getenv('CCC_DATA_DIR', default='/tmp/mmda-ccc-cache/'))
ANYCACHE_DIR = str(getenv('ANYCACHE_DIR', '/tmp/mmda-anycache/'))

# HOST AND PORT
APP_HOST = str(getenv('HOST', default='0.0.0.0'))
APP_PORT = int(getenv('PORT', default='5000'))

# TLS SETTINGS
APP_TLS_ENABLE = bool(getenv('TLS_ENABLE', default=False))
APP_TLS_KEYFILE = str(getenv('TLS_KEYFILE', default='/var/local/key.pem'))
APP_TLS_CERTFILE = str(getenv('TLS_CERTFILE', default='/var/local/cert.pem'))

# NUMBER OF PROCESSES FOR MULTIPROCESSING (only used when caching marginals)
APP_PROCESSES = int(getenv('PROCESSES', default=16))


#################
# FIXED SETTINGS
#################
APP_NAME = "MMDA Backend"

# DO NOT USE "DEBUG = True" IN PRODUCTION ENVIRONMENTS
DEBUG = False if APP_ENV == 'production' else True

# JWT Settings (seconds)
JWT_ACCESS_TOKEN_EXPIRES = 60*60*12 if APP_ENV == 'production' else False
JWT_REFRESH_TOKEN_EXPIRES = 60*60*12 if APP_ENV == 'production' else False
WTF_CSRF_ENABLED = False        # False since we're using JWT

# Application settings
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"
APP_LOG_FILE = None

# Avoid SQLAlchemy deprecation warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
