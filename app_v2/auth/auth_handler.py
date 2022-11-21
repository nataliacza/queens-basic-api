from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from config import settings
from schemas import AccessToken


def encode_jwt(username: str) -> AccessToken:
    headers = {
        "alg": settings.token_algorithm,
        "typ": settings.token_type
    }

    payload = {
        "exp": datetime.utcnow() + timedelta(days=0, minutes=float(settings.jwt_expiry_minutes)),
        "iat": datetime.utcnow(),
        "iss": settings.token_issuer,
        "scope": "access_token",
        "sub": username
    }
    token = jwt.encode(payload=payload, headers=headers, key=settings.jwt_secret,
                       algorithm=settings.token_algorithm)

    return AccessToken(token=token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, issuer=settings.token_issuer, key=settings.jwt_secret,
                                   algorithms=[settings.token_algorithm])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


def encode_password(password):
    hasher = CryptContext(schemes=["bcrypt"])
    return hasher.hash(password)


def verify_password(password, encoded_password):
    hasher = CryptContext(schemes=["bcrypt"])
    return hasher.verify(password, encoded_password)
