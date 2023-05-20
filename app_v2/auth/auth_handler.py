from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from config import settings
from schemas.auth import AccessToken

_hasher = CryptContext(schemes=["bcrypt"])


def encode_jwt(username: str) -> AccessToken:
    headers = {"alg": settings.token_algorithm, "typ": settings.token_type}

    payload = {
        "exp": datetime.utcnow()
        + timedelta(days=0, minutes=float(settings.jwt_expiry_minutes)),
        "iat": datetime.utcnow(),
        "iss": settings.token_issuer,
        "scope": "access_token",
        "sub": username,
    }
    token = jwt.encode(
        payload=payload,
        headers=headers,
        key=settings.jwt_secret,
        algorithm=settings.token_algorithm,
    )

    return AccessToken(token=token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token,
            issuer=settings.token_issuer,
            key=settings.jwt_secret,
            algorithms=[settings.token_algorithm],
        )
        return decoded_token
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=403, detail="Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=403, detail="Invalid token") from exc


def encode_password(password):
    return _hasher.hash(password)


def verify_password(password, encoded_password):
    return _hasher.verify(password, encoded_password)
