import jwt
from config import config
from datetime import datetime,timedelta


def encode_token(data: dict) -> str:

    return jwt.encode(payload=data, key=config['JWT_KEY'], algorithm='HS256')


def decode_token(token: str) -> dict:

    return jwt.decode(jwt=token, key=config['JWT_KEY'], algorithms=['HS256'])
