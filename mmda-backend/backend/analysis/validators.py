"""
For Flask API data validation.
Contains data models for the Endpoint validation
"""

LOGIN_SCHEMA = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string', 'maxLength': 64},
        'password': {'type': 'string', 'maxLength': 64},
    },
    'required': ['username', 'password']
}

PASSWORD_SCHEMA = {
    'type': 'object',
    'properties': {
        'password': {'type': 'string','minLength': 8, 'maxLength': 64}
    },
    'required': ['password']
}

USER_SCHEMA = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string', 'maxLength': 64},
        'password': {'type': 'string', 'minLength': 8, 'maxLength': 64},
        'last_name': {'type': 'string', 'maxLength': 64},
        'first_name': {'type': 'string', 'maxLength': 64},
        'email': {'type': 'string', 'format': 'email'},
        'roles': {
            'type': 'array',
            'items': {
                'type': 'string', 'maxLength': 64
            }
        }
    },
    'required': ['username', 'password', 'last_name', 'first_name', 'email']
}

USER_UPDATE_SCHEMA = {
    'type': 'object',
    'properties': {
        'last_name': {'type': 'string', 'maxLength': 64},
        'first_name': {'type': 'string', 'maxLength': 64},
        'email': {'type': 'string', 'format': 'email'}
    },
    'required': ['last_name', 'first_name', 'email']
}

ANALYSIS_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', 'maxLength': 64},
        'corpus': {'type': 'string', 'maxLength': 64},
        'window_size': {'type': 'number', 'minimum': 3, 'maximum': 20},
        'items': {
            'type': 'array',
            'items': {
                'type': 'string', 'maxLength': 64
            }
        }
    },
    'required': ['name', 'corpus', 'items']
}

UPDATE_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', 'maxLength': 64}
    },
    'required': ['name']
}

DISCOURSEME_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', 'maxLength': 64},
        'items': {
            'type': 'array',
            'items': {
                'type': 'string', 'maxLength': 64
            }
        }
    },
    'required': ['name', 'items']
}

DISCURSIVE_POSITION_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', 'maxLength': 64},
        'discoursemes': {
            'type': 'array',
            'items': {
                'type': 'number', 'minimum': 0
            }
        }
    },
    'required': ['name']
}