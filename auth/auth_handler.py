import jwt

from pathlib import Path
from functools import wraps
from http import HTTPStatus
from models.user import User
from flask import jsonify, make_response, request
from datetime import datetime, timedelta

from utils.yaml_reader import read_yaml

config_dict = read_yaml(Path('config.yaml'))

def set_token(user: User):
    return jwt.encode({
        'id': str(user.id),
        'exp' : datetime.utcnow() + timedelta(minutes = 30)
    }, config_dict['secret_key'])

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return make_response(jsonify({
                'message' : 'Token is missing!'
            }), HTTPStatus.UNAUTHORIZED)
        try:
            data = jwt.decode(
                token.split(' ')[-1], 
                config_dict['secret_key'], 
                algorithms=['HS256'])
            current_user = User.objects(id=data['id']).first()
            if not current_user:
                raise Exception()
        except Exception as e:
            return make_response(jsonify({
                'message' : 'Token is invalid!'
            }), HTTPStatus.UNAUTHORIZED)
        return  f(*args, **kwargs)
    return decorated