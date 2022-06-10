from flask import request
from flask_restx import Resource, Namespace, abort
from project.schemas import UserSchema
from project.container import user_service, auth_service
from project.exceptions import ItemNotFound

user_ns = Namespace('user')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UserView(Resource):
    @auth_service.auth_required
    @user_ns.response(200, 'OK')
    @user_ns.response(404, 'User not Found')
    def get(self):
        try:
            req_data = request.headers['Authorization']
            token = req_data.split("Bearer ")[-1]
            email = auth_service.get_user_email_from_token(token)

            user = user_service.get_user_by_email(email)
            return user_schema.dump(user), 200
        except ItemNotFound:
            abort(404, 'User not found')

    @auth_service.auth_required
    @user_ns.response(200, 'OK')
    @user_ns.response(404, 'User not Found')
    def patch(self):
        try:
            req_data = request.headers['Authorization']
            token = req_data.split("Bearer ")[-1]
            email = auth_service.get_user_email_from_token(token)

            updated_data = user_schema.dump(request.json)
            user_service.update_data(updated_data, email)
            return "", 200

        except ItemNotFound:
            abort(404, 'User not found')


@user_ns.route('/password/')
class PasswordView(Resource):
    @auth_service.auth_required
    @user_ns.response(200, 'OK')
    @user_ns.response(404, 'User not Found')
    def put(self):
        try:
            req_data = request.headers['Authorization']
            token = req_data.split("Bearer ")[-1]
            email = auth_service.get_user_email_from_token(token)

            data = request.json
            user_service.update_password(data, email)
            return "", 200
        except ItemNotFound:
            abort(404, 'User not found')
