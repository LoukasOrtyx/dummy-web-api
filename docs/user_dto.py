from docs.namespace import Namespace, fields

class UserDto:
    api = Namespace('user', description='User related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='User email address'),
        'name': fields.String(required=True, description='User name'),
        'password': fields.String(required=True, description='User password'),
        'id': fields.String(required=False, description='User Identifier')
    })
    login = api.model('login', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password'),
    })