import jwt
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta

from config import settings


class Auth:
    hasher = CryptContext(schemes=["bcrypt"])
    secret = settings.jwt_secret

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, username):
        expiry_min = settings.jwt_expiry_minutes
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=float(expiry_min)),
            "iat": datetime.utcnow(),
            "scope": "access_token",
            "sub": username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm=settings.jwt_algorithm
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[settings.jwt_algorithm])
            if payload["scope"] == "access_token":
                return payload["sub"]
            raise HTTPException(status_code=401, detail="Scope for the token is invalid")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


security = HTTPBearer()
auth_handler = Auth()
