from http import HTTPStatus
import json
from models.users import Users
from flask import Blueprint, request, jsonify

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/', methods=['GET'])
def get():
    name = request.args.get('username')
    user = Users.objects(name=name).first()
    if not user:
        return jsonify({'error': 'user not found'}), HTTPStatus.NOT_FOUND
    return jsonify(user.to_json()), HTTPStatus.OK


@users_bp.route('/', methods=['PUT'])
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
    user = Users(**payload)
    user.save()
    return jsonify(user.to_json()), HTTPStatus.OK