import bcrypt
from http import HTTPStatus
from models.users import Users
from flask import Blueprint, request, jsonify
from auth.auth_handler import set_token, token_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

def hash_pwd(pwd):
    byte_pwd = pwd.encode('utf-8')
    mySalt = bcrypt.gensalt()
    return bcrypt.hashpw(byte_pwd, mySalt)

@users_bp.route('/', methods=['GET'])
@token_required
def get():
    name = request.args.get('name')
    user = Users.objects(name=name).first()
    if not user:
        return jsonify({'error': 'user not found'}), HTTPStatus.NOT_FOUND
    return jsonify(user.to_json()), HTTPStatus.OK

@users_bp.route('/', methods=['PUT'])
@token_required
def put():
    payload = request.json
    name = payload["name"]
    user = Users.object(name=name).first()
    if not user:
        return jsonify({'error': 'user not found'}), HTTPStatus.NOT_FOUND
    payload["id"] = user.id
    user.update(**payload)
    return "", HTTPStatus.NO_CONTENT

@users_bp.route('/', methods=['DELETE'])
@token_required
def delete():
    payload = request.json
    user = Users.objects(name=payload['name']).first()
    if not user:
        return jsonify({'error': 'user not found'}), HTTPStatus.NOT_FOUND
    user.delete()
    return "", HTTPStatus.NO_CONTENT


@users_bp.route('/', methods=['POST'])
def post():
    payload = request.json
    user = Users.objects(name=payload['name']).first()
    if user:
        return jsonify({'error': 'user already exists'}), HTTPStatus.CONFLICT
    payload['password'] = hash_pwd(payload['password'])
    user = Users(**payload)
    user.save()
    auth_token = user.encode_auth_token(user.id)
    return jsonify(user.to_json()), HTTPStatus.OK, {"Authorization": auth_token.decode()}

@users_bp.route('/login', methods=['POST'])
def login():
    payload = request.json
    user = Users.objects(name=payload['name']).first()
    if not user:
        return jsonify({'error': 'user not found'}), HTTPStatus.NOT_FOUND
    pwd = payload['password'].encode('utf-8')
    if not bcrypt.checkpw(pwd, user.password.encode('utf-8')):
        return jsonify({'error': 'wrong password'}), HTTPStatus.FORBIDDEN
    token = set_token(user)
    return jsonify(user.to_json()), HTTPStatus.OK, {'Authorization': f'Bearer {token}'}