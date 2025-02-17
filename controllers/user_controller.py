import bcrypt
from http import HTTPStatus

from models.user import User
from flask_restx import Resource
from docs.user_dto import UserDto
from flask import make_response, request, jsonify
from auth.auth_handler import token_required, set_token


api = UserDto.api
_user = UserDto.user
_login = UserDto.login

auth_header = {'Authorization': 'The personal access token.'}

req_header = api.parser()
req_header.add_argument('Authorization', location='headers')

name_parser = api.parser()
name_parser.add_argument('name', type=str, help='User Name')

def hash_pwd(pwd):
    byte_pwd = pwd.encode('utf-8')
    mySalt = bcrypt.gensalt()
    return bcrypt.hashpw(byte_pwd, mySalt)

@api.route('')
class UserController(Resource):
    @api.expect(req_header, name_parser)
    @api.doc('Get a list of users', params={'name': 'The name of the user (optional)'})
    @api.response(HTTPStatus.NOT_FOUND, 'User not found.')
    @api.response(HTTPStatus.OK, "User model", model=[_user])
    @token_required
    def get(self):
        name = request.args.get('name', None)
        if name == None: 
            users = [user.to_json() for user in User.objects.all()]
        else:
            users = [user.to_json() for user in User.objects(name=name).all()]
        if not users:
            return make_response("No user was not found.", HTTPStatus.NOT_FOUND)
        return make_response(jsonify(users), HTTPStatus.OK)

    @api.expect(req_header, _user)
    @api.doc('Update an user')
    @api.response(HTTPStatus.NOT_FOUND, 'User not found.')
    @api.response(HTTPStatus.NO_CONTENT, '')
    @token_required
    def put(self):
        payload = request.json
        name = payload["name"]
        user = User.objects(name=name).first()
        if not user:
            return make_response("User was not found.", HTTPStatus.NOT_FOUND)
        payload["id"] = user.id
        user.update(**payload)
        return make_response("", HTTPStatus.NO_CONTENT)

    @api.expect(req_header, _user)
    @api.doc('Delete an user')
    @api.response(HTTPStatus.NOT_FOUND, 'User not found.')
    @api.response(HTTPStatus.NO_CONTENT, '')
    @token_required
    def delete(self):
        payload = request.json
        user = User.objects(name=payload['name']).first()
        if not user:
            return make_response("User was not found.", HTTPStatus.NOT_FOUND)
        user.delete()
        return make_response("", HTTPStatus.NO_CONTENT)

    @api.expect(_user)
    @api.doc('Create an user')
    @api.response(HTTPStatus.CONFLICT, 'User already exists.')
    @api.response(HTTPStatus.OK, "User model", model=_user, headers=auth_header)
    def post(self):
        payload = request.json
        user = User.objects(name=payload['name']).first()
        if user:
            return make_response("User already exists.", HTTPStatus.CONFLICT)
        payload['password'] = hash_pwd(payload['password'])
        user = User(**payload)
        user.save()
        token = set_token(user)
        return make_response(jsonify(user.to_json()), {"Authorization": f'Bearer {token}'})

@api.route('/login')
class LoginController(Resource):
    @api.expect(_login)
    @api.doc('Login an user')
    @api.response(HTTPStatus.NOT_FOUND, 'User not found.')
    @api.response(HTTPStatus.FORBIDDEN, 'Wrong password.')
    @api.response(HTTPStatus.OK, "User model", model=_user, headers=auth_header)
    def post(self):
        payload = request.json
        user = User.objects(email=payload['email']).first()
        if not user:
            return make_response('User not found.', HTTPStatus.NOT_FOUND)
        pwd = payload['password'].encode('utf-8')
        if not bcrypt.checkpw(pwd, user.password.encode('utf-8')):
            return make_response('Wrong password', HTTPStatus.FORBIDDEN)
        token = set_token(user)
        return make_response(jsonify(user.to_json()), {'Authorization': f'Bearer {token}'})