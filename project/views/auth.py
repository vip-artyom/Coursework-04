from flask import request
from flask_restx import Resource, Namespace, abort
from project.container import auth_service, user_service
from project.exceptions import UserAlreadyExists, ItemNotFound, InvalidToken
from project.views.users import user_schema

auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class AuthView(Resource):
    @auth_ns.response(201, 'OK')
    @auth_ns.response(404, 'Not found')
    @auth_ns.response(400, 'UserAlreadyExists')
    def post(self):
        data = {
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }
        if None in data.values():
            abort(404, 'Not found')

        try:
            data = user_schema.load(data)
            user_service.create(data)
            return "", 201
        except UserAlreadyExists:
            abort(400, 'User already exists')


@auth_ns.route('/login/')
class AuthView(Resource):
    @auth_ns.response(201, 'Tokens created')
    @auth_ns.response(404, 'Not Found')
    def post(self):
        data = {
            'email': request.json.get('email'),
            'password': request.json.get('password')
        }
        if None in data.values():
            abort(404, 'Not Found')

        try:
            tokens = auth_service.generate_tokens(data)
            return tokens, 201
        except ItemNotFound:
            abort(404, 'Tokens not found')

    @auth_ns.response(201, 'Tokens created')
    @auth_ns.response(401, 'Invalid token passed')
    @auth_ns.response(404, 'Not Found')
    def put(self):
        try:
            refresh_token = request.json.get('refresh_token')
            if not refresh_token:
                abort(404, 'Refresh token not found')

            tokens = auth_service.approve_refresh_token(refresh_token)
            return tokens, 201

        except InvalidToken:
            abort(401, 'Invalid token passed')
