import base64
import hashlib
import hmac

import jwt
from flask import current_app


def generate_password_digest(password: str) -> bin:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config.get('PWD_HASH_SALT'),
        iterations=current_app.config.get('PWD_HASH_ITERATIONS'),
    )


def hash_password(password: str) -> bin:

    hash_digest = generate_password_digest(password)
    encoded_password = base64.b64encode(hash_digest)

    return encoded_password


def compare_passwords(password_hash: bin, password: str) -> bool:

    decoded = base64.b64decode(password_hash)

    password_hash = generate_password_digest(password)

    is_correct = hmac.compare_digest(decoded, password_hash)
    return is_correct


def check_token(token: str) -> bool:
    try:
        jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=current_app.config.get('JWT_ALGORITHM'))
        return True
    except Exception as e:
        print(e)
        return False
