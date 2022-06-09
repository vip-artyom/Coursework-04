import base64
import hashlib
import hmac

import jwt

from project import BaseConfig


def generate_password_digest(password):
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=BaseConfig.PWD_HASH_SALT,
        iterations=BaseConfig.PWD_HASH_ITERATIONS,
    )


def hash_password(password):

    hash_digest = generate_password_digest(password)
    encoded_password = base64.b64encode(hash_digest)

    return encoded_password


def compare_passwords(password_hash, password):

    decoded = base64.b64decode(password_hash)

    password_hash = generate_password_digest(password)

    is_correct = hmac.compare_digest(decoded, password_hash)
    return is_correct


def check_token(token):
    try:
        jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=BaseConfig.JWT_ALGORITHM)
        return True
    except Exception as e:
        print(e)
        return False
