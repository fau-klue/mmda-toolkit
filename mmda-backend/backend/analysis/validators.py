"""
For Flask API data validation.
Contains data models for the Endpoint validation
"""


ANALYSIS_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'corpus': {'type': 'string'},
        'window_size': {'type': 'number'},
        'items': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        }
    },
    'required': ['name', 'corpus', 'items']
}

ANALYSIS_UPDATE_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'}
    },
    'required': ['name']
}

DISCOURSEME_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'items': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        }
    },
    'required': ['name', 'items']
}

DISCURSIVE_POSITION_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'discoursemes': {
            'type': 'array',
            'items': {
                'type': 'number'
            }
        }
    },
    'required': ['name']
}
