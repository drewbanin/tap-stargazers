user = {
    'type': 'object',
    'properties': {
        'id': {
            'type': 'number',
            'description': 'id for the user',
        },
        'login': {
            'type': 'string',
            'description': 'login for the user',
        },
        'avatar_url': {
            'type': 'string',
            'description': 'avatar url for the user',
        },
        'url': {
            'type': 'string',
            'description': 'url link for the user',
        },
        'type': {
            'type': 'string',
            'description': 'user type',
        },
    }
}

star = {
    'type': 'object',
    'properties': {
        'starred_at': {
            'type': ['string', 'null'],
            'format': 'date-time',
            'description': 'When the repo was starred',
        },
        'user': user
    }
}
