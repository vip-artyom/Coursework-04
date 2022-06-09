import datetime
import calendar

import jwt
from flask import request
from flask_restx import abort

from .user_service import UserService
from ..config import BaseConfig
from ..exceptions import IncorrectPassword, InvalidToken
from ..tools import compare_passwords


class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, data_info, is_refresh=False):

        email = data_info.get('email')
        password = data_info.get('password')

        user = self.user_service.get_user_by_email(email)

        if not user:
            abort(404)

        if not is_refresh:
            correct_password = compare_passwords(user.password, password)
            if not correct_password:
                raise IncorrectPassword

        data = {
            'email': user.email
        }

        min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=BaseConfig.TOKEN_EXPIRE_MINUTES)
        data['exp'] = calendar.timegm(min15.timetuple())
        access_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=BaseConfig.TOKEN_EXPIRE_DAYS)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.JWT_ALGORITHM)

        tokens = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return tokens

    @staticmethod
    def get_user_email_from_token(token):
        try:
            data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.JWT_ALGORITHM])
            email = data.get('email')
            return email
        except Exception:
            raise InvalidToken

    def approve_refresh_token(self, refresh_token):

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
                jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.JWT_ALGORITHM])
            except Exception as e:
                abort(401, f'JWT error {e}')

            return func(*args, **kwargs)

        return wrapper
