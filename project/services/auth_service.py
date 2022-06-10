import datetime
import calendar

import jwt
from flask import request, current_app
from flask_restx import abort

from .user_service import UserService
from ..exceptions import IncorrectPassword, InvalidToken
from ..tools import compare_passwords


class AuthService:

    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def generate_tokens(self, data_info: dict, is_refresh=False) -> dict:

        email = data_info.get('email')
        password = data_info.get('password')

        find_user = self.user_service.get_user_by_email(email)

        if not find_user:
            abort(404)

        if not is_refresh:
            correct_password = compare_passwords(find_user.password, password)
            if not correct_password:
                raise IncorrectPassword

        data = {
            'email': find_user.email
        }

        min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config.get('TOKEN_EXPIRE_MINUTES'))
        data['exp'] = calendar.timegm(min15.timetuple())
        access_token = jwt.encode(data, current_app.config.get('SECRET_KEY'),
                                  algorithm=current_app.config.get('JWT_ALGORITHM'))

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config.get('TOKEN_EXPIRE_DAYS'))
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, current_app.config.get('SECRET_KEY'),
                                   algorithm=current_app.config.get('JWT_ALGORITHM'))

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    @staticmethod
    def get_user_email_from_token(token: str) -> str:
        try:
            data = jwt.decode(token, current_app.config.get('SECRET_KEY'),
                              algorithms=[current_app.config.get('JWT_ALGORITHM')])
            email = data.get('email')
            return email
        except Exception:
            raise InvalidToken

    def approve_refresh_token(self, refresh_token: str) -> dict:

        data = {
            'email': self.get_user_email_from_token(refresh_token),
            'password': None
        }
        new_tokens = self.generate_tokens(data, is_refresh=True)

        return new_tokens

    @staticmethod
    def auth_required(func):

        def wrapper(*args, **kwargs):
            if 'Authorization' not in request.headers:
                abort(401, 'Authorization is None')

            data = request.headers['Authorization']
            token = data.split("Bearer ")[-1]

            try:
                jwt.decode(token, current_app.config.get('SECRET_KEY'),
                           algorithms=[current_app.config.get('JWT_ALGORITHM')])
            except Exception as e:
                abort(401, f'JWT error {e}')

            return func(*args, **kwargs)

        return wrapper
